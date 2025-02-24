
# ConsultarRuc

Api para ConsultarRuc desde soap





## Instalacion

Install ConsultarRuc with pip

```bash
  pip install flask lxml requests bs4
```

## Ejecutar

Ejecutar ConsultarRuc 

```bash
  python ConsultarRuc.py
```

## Salida

http://127.0.0.1:8000/soap/wsdl

```bash
  This XML file does not appear to have any style information associated with it. The document tree is shown below.
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="http://example.com/consultaruc" xmlns:xsd="http://www.w3.org/2001/XMLSchema" name="ConsultaRucService" targetNamespace="http://example.com/consultaruc">
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
```
    
