from flask import Blueprint, jsonify, request
from models.usuario import ErroCadastro 
from services.cadastro_service import CadastroService

cadastro_bp = Blueprint ("cadastro", __name__, url_prefix="/api/cadastro")
def _get_service() -> CadastroService:
    from flask import current_app
    return current_app.config["CADASTRO_SERVICE"]
@cadastro_bp.post("/")
def cadastrar():
    dados = request.get_json(silent=True) or {}
    campos_obrigatorios = ["nome", "email", "cpf", "senha"]
    ausentes = [c for c in campos_obrigatorios if not dados.get(c)]
    if ausentes: 
        return jsonify({"erro": "Campos obrigatorios ausentes", "campos": ausentes}), 422
    
    try:
        usuario = _get_service().cadastrar(
            nome=dados["nome"],
            email=dados["email"],
            cpf=dados["cpf"],
            senha=dados["senha"],
        )
        
        return jsonify({"mensagem": "Usuario cadastrado com sucesso.", "usuario": usuario}),201
    
    except ErroCadastro as e:
        return jsonify(e.to_dict()), 400
    
@cadastro_bp.post("/gerar-senha")
def cadastrar_com_senha_gerada():
    dados = request.get_json(silent=True) or {}
    campos_obrigatorios = ["nome", "email", "cpf"]
    ausentes = [c for c in campos_obrigatorios if not dados.get(c)]
    if ausentes:
        return jsonify({"erro": "Campos obrigatórios ausentes", "campos": ausentes}), 422
    
    try:
        resultado = _get_service().cadastrar_com_senha_gerada(
            nome=dados["nome"],
            email=dados["email"],
            cpf=dados["cpf"],
        )
        return jsonify({
            "mensagem": "Usuário cadastrado. Guarde a senha temporária, ela não sera exibida de novo.",
            "senha": resultado,
        }), 201
    except ErroCadastro as e:
        return jsonify(e.to_dict()), 400
    