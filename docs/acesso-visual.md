# Entrada visual da apresentação

`index.html` apresenta o formulário de acesso e abre `home.html` após uma animação.
Usuário de demonstração: `contato@yvyagro.com`. A senha aleatória foi entregue
separadamente ao responsável; o HTML guarda apenas seu resumo SHA-256.

Isso **não é autenticação**: o JavaScript é público, o formulário pode ser
contornado e o endereço `home.html` continua acessível diretamente. Não protege
informações confidenciais. O hash evita somente expor a senha em texto literal;
não transforma a barreira visual em controle de acesso.

A verificação usa Web Crypto, disponível no GitHub Pages via HTTPS. Não há
servidor, sessão, coleta ou envio de credenciais. O navegador pode oferecer
salvá-las por meio de seu gerenciador de senhas.
Erro aparece no formulário; há opção de mostrar senha e transição de abertura
com respeito à preferência por movimento reduzido.

O arquivo index resolve a ausência de página inicial no GitHub Pages sem duplicar
o configurador canônico. Não é necessário configurar outra rota na hospedagem.
