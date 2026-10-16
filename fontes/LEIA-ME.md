# Fontes do Conversor CA Marluvas (Chamae)

Este repositório publica o app pronto (criptografado). Os **arquivos de trabalho** (código-fonte editável,
catálogo com preços, clientes, scripts de montagem) ficam em `fontes/marluvas.tar.gz.enc`,
criptografado com a **senha da equipe** (a mesma do app). Sem a senha o arquivo é ilegível.

## Restaurar os fontes (para continuar o desenvolvimento em qualquer conversa/computador)
```
python3 fontes/backup_fontes.py restaurar fontes/marluvas.tar.gz.enc ./fontes-marluvas
```
(requer `pip install cryptography`; pede a senha da equipe)

## Estrutura (depois de restaurar)
- `app/template_teste.html` — código-fonte do app (versão em teste; é a fonte principal)
- `app/template.html` — cópia aprovada que vai para o oficial
- `app/cat4.json` catálogo/preços · `app/clientes.json` clientes · `app/grd.json` grades/embalagem · `app/reprio_ids.json` IDs Reprio
- `buildpwa2.py` monta e criptografa · `publicar.sh teste|oficial` monta e copia para o clone deste repo (variável REPO)
- `backup_fontes.py` gera/restaura este backup

## Fluxo de trabalho
1. Toda mudança vai primeiro para **/teste/** (`./publicar.sh teste`, commit, push).
2. Só após aprovação do Victor: `./publicar.sh oficial`, commit, push.
3. Depois de cada publicação, **regerar o backup**: `python3 backup_fontes.py backup . <repo>/fontes/marluvas.tar.gz.enc` e commitar.

## Automações (GitHub Actions)
- `sync-drive.yml` (15 em 15 min): fichas técnicas e imagens da pasta do Drive + imagens faltantes do site Marluvas.
- `caepi.yml` (segundas): baixa a base CAEPI do Ministério e gera `caepi.json` (só calçados).
- `fotos-ca.yml` (segundas): fotos dos CAs concorrentes (consultaca.com) em `img_ca/` + `caepi_fotos.json`.

## Regras de negócio (resumo)
- Preço = Tabela Geral SP com desconto do canal; cliente sem tabela usa REV60-518.
- Prazo: acréscimo conforme lista oficial de prazos (à vista −2%; 7/14/21 = 0%; ... teto 6%).
- Frete somente CIF; pedido mínimo R$ 3.500 por pedido; MTS e MTO são faturados separados
  (no Reprio vai 1 rascunho único com itens marcados [MTS]/[MTO] para separar na transmissão).
- ICMS: 18% MG; 12% SP/RJ/PR/SC/RS; 7% demais.
- Reprio: preço com encargo do prazo já embutido; grade vai nas observações; vendedores: Drauzio, Igor, Victor.
- Interpretação de CA concorrente: altura (Tipo A–E do CAEPI), segurança × ocupacional, "Aprovado para",
  cores do campo oficial; validada contra os CAs da própria Marluvas (~99% de acerto de classe).
