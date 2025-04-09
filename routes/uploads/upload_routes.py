from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import send_from_directory, abort
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import os

from models import db, Animal, ImagemAnimal
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.uploader import upload

upload_routes = Blueprint('upload_routes', __name__)

@upload_routes.route("/upload_cloudinary", methods=["POST"])
@jwt_required()
def upload_para_cloudinary():
    usuario_id = get_jwt_identity()

    if 'imagem' not in request.files or 'animal_id' not in request.form:
        return jsonify({"message": "Imagem e animal_id são obrigatórios"}), 400

    imagem = request.files['imagem']
    animal_id = request.form['animal_id']

    try:
        resultado = upload(imagem, folder=f"mrzoo/usuario_{usuario_id}//animal_{animal_id}/")
        url = resultado.get("secure_url")

        animal = Animal.query.filter_by(id=animal_id, usuario_id=usuario_id).first()

        if not animal:
           return jsonify({"message": "Animal não encontrado ou não pertence ao usuário!"}), 404

        # Pegando a URL direto do campo do form
        animal.imagem_url = url
        db.session.commit()

        return jsonify({"url": url}), 200
    except Exception as e:
        print(f"Erro ao enviar para o Cloudinary: {e}")
        return jsonify({"erro": "Falha no upload"}), 500


@upload_routes.route("/upload_cloudinary_multiplas", methods=["POST"])
@jwt_required()
def upload_multiplas_cloudinary():
    usuario_id = get_jwt_identity()
    animal_id = request.form.get("animal_id")

    if not animal_id:
        return jsonify({"erro": "animal_id é obrigatório"}), 400

    arquivos = request.files.getlist("imagens")
    if not arquivos:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    urls_salvas = []

    try:
        for imagem in arquivos:
            if imagem:
                resultado = upload(
                    imagem,
                    folder=f"mrzoo/usuario_{usuario_id}/animal_{animal_id}/",
                    public_id=f"{animal_id}_{uuid.uuid4().hex[:6]}"
                )
                url = resultado.get("secure_url")
                urls_salvas.append(url)

                nova_imagem = ImagemAnimal(
                    animal_id=animal_id,
                    url=url,
                    data_upload=datetime.utcnow()
                )
                db.session.add(nova_imagem)

        db.session.commit()
        return jsonify({"mensagem": "Imagens salvas com sucesso", "imagens": urls_salvas}), 200

    except Exception as e:
        print(f"Erro ao enviar para Cloudinary: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500
    
    
@upload_routes.route('/uploads/usuarios/usuario_<int:usuario_id>/animais/animal_<int:animal_id>/<filename>')
def servir_foto_animal(usuario_id, animal_id, filename):
    diretorio_destino = os.path.join("uploads", "usuarios", f'usuario_{usuario_id}', f'animal_{animal_id}')

        # Segurança extra: impede acesso a arquivos fora da pasta
    if not os.path.isfile(os.path.join(diretorio_destino, filename)):
        return abort(404)
    
    return send_from_directory(diretorio_destino, filename)


@upload_routes.route('/uploads/images/usuario_<int:usuario_id>/animal_<int:animal_id>/<filename>')
def servir_imagem(usuario_id, animal_id, filename):
    caminho = os.path.join('uploads', 'images', f'usuario_{usuario_id}', f'animal_{animal_id}')

    # Segurança extra: impede acesso a arquivos fora da pasta
    if not os.path.isfile(os.path.join(caminho, filename)):
        return abort(404)

    return send_from_directory(caminho, filename)

@upload_routes.route("/upload_imagens_animal", methods=["POST"])
@jwt_required()
def upload_imagens_animal():
    try:
        usuario_id = get_jwt_identity()
        animal_id = request.form.get("animal_id")
        imagens = request.files.getlist("imagens")

        if not animal_id:
            return jsonify({"erro": "animal_id é obrigatório"}), 400

        if not imagens:
            return jsonify({"erro": "Nenhuma imagem enviada"}), 400

        urls_salvas = []

        for imagem in imagens:
            if imagem:
                filename = f"{uuid.uuid4().hex[:6]}.jpg"

                diretorio_destino = os.path.join("uploads", "usuarios", f'usuario_{usuario_id}', f'animal_{animal_id}')
                os.makedirs(diretorio_destino, exist_ok=True)

                # Salvar com caminho completo
                caminho_completo = os.path.join(diretorio_destino, filename)
                imagem.save(caminho_completo)

                url = f"/uploads/usuarios/usuario_{usuario_id}/animais/animal_{animal_id}/{filename}"
                urls_salvas.append(url)

                nova_imagem = ImagemAnimal(
                    animal_id=animal_id,
                    url=url,
                    data_upload=datetime.utcnow()
                )
                db.session.add(nova_imagem)

        db.session.commit()
        return jsonify({"mensagem": "Imagens salvas com sucesso", "imagens": urls_salvas}), 200

    except Exception as e:
        print(f"Erro ao adicionar imagens: {e}")
        return jsonify({"message": str(e)}), 500
