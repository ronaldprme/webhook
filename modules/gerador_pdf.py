import io
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak, BaseDocTemplate, Frame, PageTemplate, NextPageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from modules.styles_config import configurar_estilos, ESPACO_TOPO_PAGINAS, ESPACO_TOPO_PAGINA_1, ESPACO_INFERIOR_TEXTO, ESPACO_RODAPE
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
from datetime import datetime



styles = configurar_estilos()

plt.rcParams['font.family'] = 'Liberation Sans'

def gerar_grafico_pontuacao(pontuacao):
    faixas = [0, 75, 150, 225, 300]
    labels = ["Leve", "Moderado", "Significativo", "Severo"]
    cores = ["#a8e6cf", "#ffd3b6", "#ffaaa5", "#ff8b94"]
    
	# Carrega explicitamente a fonte Liberation Sans
    font_prop = font_manager.FontProperties(family='Liberation Sans')

    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    # font_path = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"
    # font_prop = font_manager.FontProperties(fname=font_path)
    # plt.rcParams['font.family'] = font_prop.get_name()

    fig, ax = plt.subplots(figsize=(8, 1.6))

    for i in range(len(faixas) - 1):
        ax.barh(y=0, width=faixas[i+1] - faixas[i], left=faixas[i], height=0.9,
                color=cores[i], edgecolor=None)

    ax.plot(pontuacao, 0.22, "k^", markersize=15)
    ax.text(pontuacao, 0.5, f"{pontuacao}", ha="center", fontsize=10)

    for i in range(len(labels)):
        meio = (faixas[i] + faixas[i+1]) / 2
        ax.text(meio, 0.75, labels[i], ha="center", fontsize=11, weight="bold")

    ax.set_xlim(0, 300)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks(faixas)
    ax.set_title("Nível de Trauma Psicológico", fontsize=14, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.spines['top'].set_visible(False)       # Remove linha superior
    ax.spines['right'].set_visible(False)     # (opcional) Remove lateral direita
    ax.spines['left'].set_visible(False)      # (opcional) Remove lateral esquerda
    ax.spines['bottom'].set_visible(False)

	# Deixe a inferior visível se quiser manter o eixo 0 com faixas
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    plt.close()
    buffer.seek(0)
    return buffer

    plt.close()


def rodape(canvas: Canvas, doc):
    if canvas.getPageNumber() == 1:
        return

    canvas.saveState()
    canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, ESPACO_RODAPE + 10, A4[0] - doc.rightMargin, ESPACO_RODAPE + 10)
    canvas.setFont('Helvetica', 9)

    # nome_formatado = " ".join(["de" if p.lower() == "de" else p.capitalize() for p in doc.nome.split()])
    nome_completo = f"{doc.nome} {doc.sobrenome}"
    nome_formatado = " ".join(["de" if p.lower() == "de" else p.capitalize() for p in nome_completo.split()])
    try:
        data_convertida = datetime.strptime(doc.submission_date.strip(), '%b. %d, %Y').strftime('%d/%m/%Y')
    except:
        try:
            data_convertida = datetime.strptime(doc.submission_date.strip(), '%b.%d,%Y').strftime('%d/%m/%Y')
        except:
            data_convertida = doc.submission_date

    # Aplicar fonte em negrito para "Relatório Personalizado"
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(doc.leftMargin, ESPACO_RODAPE, "Relatório Personalizado:")

    canvas.setFont('Helvetica', 9)
    texto_rodape = f"{nome_formatado} | {doc.email} | {data_convertida}"
    canvas.drawString(doc.leftMargin + 110, ESPACO_RODAPE, texto_rodape)
    canvas.drawRightString(A4[0] - doc.rightMargin, ESPACO_RODAPE, f"Página {canvas.getPageNumber() - 1}")
    canvas.restoreState()

def cabecalho(canvas: Canvas, doc):
    canvas.saveState()
    if canvas.getPageNumber() > 1:
        logo_path = "data/logo.png"
        try:
            canvas.drawImage(logo_path, (A4[0] - 50) / 2, A4[1] - 90, width=50, height=50)
        except:
            pass
    canvas.restoreState()

def gerar_relatorio(nome_arquivo, nome, sobrenome, email, total, paragrafos, submission_id="", submission_date=""):
    doc = BaseDocTemplate(nome_arquivo, pagesize=A4)

    nome_limpo = " ".join(nome.strip().split())
    primeiro_nome = nome_limpo.split()[0].capitalize()

    doc.nome = nome_limpo
    doc.sobrenome = sobrenome
    doc.email = email
    # doc.submission_id = submission_id
    doc.submission_id = str(submission_id)[:7] # Retorna apenas os 7 primeiros digitos
    doc.submission_date = submission_date

    # Configuração para a primeira página
    altura_conteudo_primeira_pagina = A4[1] - (ESPACO_TOPO_PAGINA_1 + ESPACO_INFERIOR_TEXTO)
    frame_primeira_pagina = Frame(
        doc.leftMargin,
        ESPACO_INFERIOR_TEXTO,
        doc.width,
        altura_conteudo_primeira_pagina,
        id='primeira_pagina'
    )

    # Configuração para as páginas subsequentes
    altura_conteudo_paginas = A4[1] - (ESPACO_TOPO_PAGINAS + ESPACO_INFERIOR_TEXTO)
    frame_paginas = Frame(
        doc.leftMargin,
        ESPACO_INFERIOR_TEXTO,
        doc.width,
        altura_conteudo_paginas,
        id='paginas_subsequentes'
    )

    # Templates de página
    template_primeira_pagina = PageTemplate(
        id='primeira_pagina',
        frames=frame_primeira_pagina,
        onPage=rodape,
        onPageEnd=cabecalho
    )
    template_paginas = PageTemplate(
        id='paginas_subsequentes',
        frames=frame_paginas,
        onPage=rodape,
        onPageEnd=cabecalho
    )

    # Adiciona os templates ao documento
    doc.addPageTemplates([template_primeira_pagina, template_paginas])

    story = []

    # Adiciona o logo na primeira página
    logo_path = "data/logo.png"
    try:
        img = Image(logo_path, width=90, height=90)
        img.hAlign = 'CENTER'
        story.append(img)
    except Exception as e:
        print(f"[ERRO] Logo não carregada: {e}")

    # Adiciona o título e subtítulo na primeira página
    story.append(Paragraph("TESTE DE TRAUMA", styles['Titulo']))
    story.append(Paragraph("Análise Personalizada", styles['Subtitulo']))
    
    # Gerar o gráfico com base no total do cliente
    try:
        # total = int(submission_id)  # ou passe o total como argumento se preferir
       if total is not None:
            buffer = gerar_grafico_pontuacao(total)
            img_grafico = Image(buffer, width=400, height=60)
            img_grafico.hAlign = 'CENTER'
            # story.append(Spacer(1, 12))
            story.append(img_grafico)
            story.append(Spacer(1, 12))
    except Exception as e:
        print(f"[ERRO] Falha ao gerar gráfico: {e}")

	# Troca para o template das páginas subsequentes após a primeira página
    story.append(NextPageTemplate('paginas_subsequentes'))
    # story.append(PageBreak())  # Garante que a próxima página use o novo template

    primeira_pagina = True
    for p in paragrafos:
        if p == "<PAGEBREAK>":
            story.append(PageBreak())
            continue
        elif p.startswith("<<RESULTADO:>>"):
            conteudo = p.replace("<<RESULTADO:>>", "").strip()
            story.append(Paragraph(conteudo, styles['Subtitulo1']))
            story.append(Spacer(1, 1))  # Espaçamento após o parágrafo
            print(f"entrou aqui")
            continue
  
        elif p.startswith("<<SINAIS:>>"):
            conteudo = p.replace("<<SINAIS:>>", "").strip()
            story.append(Paragraph(conteudo, styles['Subtitulo1']))
            story.append(Spacer(1, 1))  # Espaçamento após o parágrafo
            continue

        elif p.startswith("<<NOME:>>"):
            conteudo = p.replace("<<NOME:>>", "").strip()
            story.append(Paragraph(conteudo, styles['TextoNormal']))
            story.append(Spacer(1, 8))  # Espaçamento após o parágrafo
            continue
            # Troca para o template das páginas subsequentes
            # story.append(NextPageTemplate('paginas_subsequentes'))
            # primeira_pagina = False
            # continue

        elif p.strip().startswith("<b>") and p.strip().endswith("</b>"):
            conteudo = p.strip()[3:-4].strip()
            story.append(Paragraph(conteudo, styles['TituloSessao']))
        elif p.startswith("<TAB>"):
            story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + p[5:], styles['Tabulado']))
        elif "Olá" in p and primeira_pagina:
            # Espaçamento específico para a primeira página
            story.append(Paragraph(f"Olá {primeiro_nome}!", styles['TextoNormal']))
            story.append(Spacer(1, 12))  # Espaçamento maior na primeira página
        else:
            story.append(Paragraph(p, styles['TextoNormal']))
            story.append(Spacer(1, 4))  # Espaçamento padrão para páginas subsequentes

     # Adiciona uma quebra de página antes da imagem final
    # story.append(PageBreak())

    # Adiciona a imagem após a última página
    imagem_final_path = "data/piramide.png"  # Substitua pelo caminho da sua imagem
    try:
        img_final = Image(imagem_final_path, width=400, height=300)  # Ajuste o tamanho conforme necessário
        img_final.hAlign = 'CENTER'
        story.append(img_final)
    except Exception as e:
        print(f"[ERRO] Imagem final não carregada: {e}")


    doc.build(story)
