from flask import Flask, request, Response
from lxml import etree
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Definir el WSDL manualmente
WSDL_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<definitions name="ConsultaRucService"
    xmlns="http://schemas.xmlsoap.org/wsdl/"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns:tns="http://example.com/consultaruc"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    targetNamespace="http://example.com/consultaruc">

    <types>
        <xsd:schema targetNamespace="http://example.com/consultaruc">
            <xsd:element name="obtenerNombrePorRucRequest">
                <xsd:complexType>
                    <xsd:sequence>
                        <xsd:element name="ruc" type="xsd:string"/>
                    </xsd:sequence>
                </xsd:complexType>
            </xsd:element>
            <xsd:element name="obtenerNombrePorRucResponse">
                <xsd:complexType>
                    <xsd:sequence>
                        <xsd:element name="nombre" type="xsd:string"/>
                    </xsd:sequence>
                </xsd:complexType>
            </xsd:element>
        </xsd:schema>
    </types>

    <message name="obtenerNombrePorRucRequest">
        <part name="parameters" element="tns:obtenerNombrePorRucRequest"/>
    </message>

    <message name="obtenerNombrePorRucResponse">
        <part name="parameters" element="tns:obtenerNombrePorRucResponse"/>
    </message>

    <portType name="ConsultaRucPortType">
        <operation name="obtenerNombrePorRuc">
            <input message="tns:obtenerNombrePorRucRequest"/>
            <output message="tns:obtenerNombrePorRucResponse"/>
        </operation>
    </portType>

    <binding name="ConsultaRucBinding" type="tns:ConsultaRucPortType">
        <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
        <operation name="obtenerNombrePorRuc">
            <soap:operation soapAction="http://example.com/consultaruc/obtenerNombrePorRuc"/>
            <input>
                <soap:body use="literal"/>
            </input>
            <output>
                <soap:body use="literal"/>
            </output>
        </operation>
    </binding>

    <service name="ConsultaRucService">
        <port name="ConsultaRucPort" binding="tns:ConsultaRucBinding">
            <soap:address location="http://localhost:8000/soap"/>
        </port>
    </service>
</definitions>
"""

# Función para obtener el nombre de la empresa desde SUNAT
def obtener_nombre_por_ruc(ruc):
    api_url = f"https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&razSoc=&nroRuc={ruc}&nrodoc=&token=1&contexto=ti-it&modo=1&rbtnTipo=1&search1={ruc}&tipdoc=1&search2=&search3=&codigo="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/'
    }

    try:
        response = requests.post(api_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer razón social (nombre legal de la empresa)
            razon_social = soup.find('h4', class_='list-group-item-heading', text=lambda t: t and 'Número de RUC:' in t)
            if razon_social:
                razon_social = razon_social.find_next('h4', class_='list-group-item-heading').get_text(strip=True)
                razon_social = razon_social.split(" - ", 1)[1]  # Extraer solo el nombre

            # Extraer nombre comercial
            nombre_comercial_tag = soup.find('h4', text="Nombre Comercial:")
            if nombre_comercial_tag:
                nombre_comercial = nombre_comercial_tag.find_next('p', class_='list-group-item-text').get_text(strip=True)
            else:
                nombre_comercial = "No registrado"

            return {
                "RUC": ruc,
                "Razón Social": razon_social if razon_social else "No encontrado",
                "Nombre Comercial": nombre_comercial
            }
        else:
            return {"error": f"❌ Error {response.status_code} al consultar el RUC {ruc}"}
        
    except Exception as e:
        return f"Error: {e}"

# Ruta para obtener el WSDL
@app.route('/soap/wsdl', methods=['GET'])
def wsdl():
    return Response(WSDL_TEMPLATE, mimetype='text/xml')

# Ruta para manejar solicitudes SOAP
@app.route('/soap', methods=['POST'])
def soap():
    """ Procesa la solicitud SOAP y devuelve la respuesta en formato SOAP """
    try:
        xml_request = request.data
        tree = etree.fromstring(xml_request)

        # Extraer el RUC del XML de la solicitud
        namespace = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
        body = tree.find('.//soap:Body', namespace)
        ruc_node = body.find('.//ruc')
        
        if ruc_node is not None:
            ruc = ruc_node.text
            datos = obtener_nombre_por_ruc(ruc)

            # Crear la respuesta SOAP con cada campo por separado
            response_template = f"""<?xml version="1.0" encoding="UTF-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <obtenerNombrePorRucResponse xmlns="http://example.com/consultaruc">
                        <ruc>{datos.get('RUC', 'No encontrado')}</ruc>
                        <razon_social>{datos.get('Razón Social', 'No encontrado')}</razon_social>
                        <nombre_comercial>{datos.get('Nombre Comercial', 'No registrado')}</nombre_comercial>
                    </obtenerNombrePorRucResponse>
                </soap:Body>
            </soap:Envelope>"""
            
            return Response(response_template, mimetype='text/xml')
        
        return Response("RUC no encontrado en la solicitud", status=400)
    
    except Exception as e:
        return Response(f"Error procesando la solicitud: {e}", status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)