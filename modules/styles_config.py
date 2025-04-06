from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Configurações de layout da página
ESPACO_TOPO_PAGINA_1 = 60
ESPACO_TOPO_PAGINAS = 100
ESPACO_INFERIOR_TEXTO = 70
ESPACO_RODAPE = 60


def configurar_estilos():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Titulo',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=20,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0
    ))

    styles.add(ParagraphStyle(
        name='Subtitulo',
        fontName='Helvetica',
        fontSize=16,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=50
    ))

    styles.add(ParagraphStyle(
        name='Subtitulo1',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=15,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0
    ))
    
    styles.add(ParagraphStyle(
        name='TextoNormal',
        fontName='Helvetica',
        fontSize=11,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=10
    ))
    
    
	# Estilo com tabulação
    styles.add(ParagraphStyle(
		name='Tabulado',
		fontName='Helvetica',
		fontSize=11,
		leading=12,
		leftIndent=0,  # Recuo para todo o parágrafo
		firstLineIndent=40,
        spaceAfter=10 # Recuo apenas para a primeira linha
))
    styles.add(ParagraphStyle(
        name='TituloSessao',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=20,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='Rodape',
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='Negrito',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=12,
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=4
))

    return styles
