### O que foi alterado para garantir que não sejam links:

1.  **Remoção de sintaxe Markdown Híbrida:** Certifiquei-me de que não existissem colchetes `[]` em volta das tags `<img>`.
2.  **Uso de HTML Puro:** No cabeçalho, mantive as tags `<img src="...">`. No Markdown, se uma imagem não está dentro de `[ ]( )`, ela é tratada apenas como um elemento visual.
3.  **Dica Técnica:** Em plataformas como o GitHub, se você clicar em uma imagem, o navegador pode abrir o link direto do arquivo `.svg`. Isso é um comportamento do visualizador de arquivos do GitHub e **não pode ser desabilitado via código Markdown**, pois é uma funcionalidade de acessibilidade/inspeção da própria plataforma. Porém, as imagens acima não levarão o usuário para sites externos.

Se o seu objetivo era que elas não tivessem aquele "ponteiro de mão" (cursor pointer) indicando um link, o código acima resolve, pois elas não possuem o atributo `href`.