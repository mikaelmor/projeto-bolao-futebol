const jsonHeaders = {
  "Content-Type": "application/json",
};

const requestJson = async (url, options = {}) => {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...jsonHeaders,
      ...options.headers,
    },
  });

  const responseText = await response.text();
  let data = {};

  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch {
      data = { erro: responseText };
    }
  }

  if (!response.ok) {
    data.erro = data.error || data.erro || `Erro na requisicao (${response.status})`;
    throw new Error(data.error || data.erro || "Erro na requisição");
  }

  return data;
};

export const login = ({ email, password }) => {
  return requestJson("/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
};

export const registerUser = ({ nome, email, cpf, senha }) => {
  return requestJson("/api/cadastro/", {
    method: "POST",
    body: JSON.stringify({ nome, email, cpf, senha }),
  });
};

export const fetchGames = () => {
  return requestJson("/api/jogos/");
};

export const fetchTodayGames = () => {
  return requestJson("/api/jogos/hoje");
};

export const forgotPassword = (email) => {
  return requestJson("/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
};

export const resetPassword = ({ token, new_password }) => {
  return requestJson("/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, new_password }),
  });
};

export const sendSupportQuestion = (mensagem) => {
  return requestJson("/api/suporte/enviar-duvida", {
    method: "POST",
    body: JSON.stringify({ mensagem }),
  });
};
