def generar_uxf(enunciado):
    nombre_archivo = "salida_generada.uxf"
    
    uxf = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<diagram program="umlet" version="14.3">
  <elements>
    <element>
      <id>UMLActor</id>
      <coordinates>
        <x>30</x>
        <y>30</y>
        <w>60</w>
        <h>60</h>
      </coordinates>
      <panel_attributes>Usuario</panel_attributes>
      <additional_attributes/>
    </element>
    <element>
      <id>UMLActor</id>
      <coordinates>
        <x>300</x>
        <y>30</y>
        <w>60</w>
        <h>60</h>
      </coordinates>
      <panel_attributes>Sistema</panel_attributes>
      <additional_attributes/>
    </element>
    <element>
      <id>UMLUseCase</id>
      <coordinates>
        <x>150</x>
        <y>150</y>
        <w>160</w>
        <h>60</h>
      </coordinates>
      <panel_attributes>{}</panel_attributes>
      <additional_attributes/>
    </element>
    <element>
      <id>UMLRelation</id>
      <coordinates>
        <x>0</x>
        <y>0</y>
        <w>0</w>
        <h>0</h>
      </coordinates>
      <panel_attributes>--</panel_attributes>
      <additional_attributes>head1=none;head2=none;line=straight;lt=--;</additional_attributes>
    </element>
    <element>
      <id>UMLRelation</id>
      <coordinates>
        <x>0</x>
        <y>0</y>
        <w>0</w>
        <h>0</h>
      </coordinates>
      <panel_attributes>--</panel_attributes>
      <additional_attributes>head1=none;head2=none;line=straight;lt=--;</additional_attributes>
    </element>
  </elements>
</diagram>
""".format(enunciado)

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(uxf)

    return nombre_archivo