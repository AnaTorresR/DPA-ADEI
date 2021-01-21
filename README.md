# DPA Food Inspections 2021

* Integrantes del equipo
  * Edgar Bazo
  * Dira Martínez
  * Iván Salgado
  * Ana Torres
  
  
* Datos a utilizar: Inspecciones a restaurantes y otros establecimientos en Chicago, estas inspecciones son realizadas por el personal del Programa de Protección de Alimentos del Departamento de Salud Pública de Chicago. 

  * **Número de registros:** 215,130 al 15 de enero del 2021
  * **Número de columnas:** 17
 
    * Inspection ID: Identificador
    
    * DBA Name: 'Doing business as', hace referencia al nombre legal del establecimiento
    
    * AKA Name: Alias del nombre del establecimiento
    
    * License #: Número único asignado al establecimiento por parte del Departamento de Asuntos Comerciales y Protección al Consumidor. 
    
    * Facility Type: Tipo de establecimiento, 500 diferentes tipos de establecimientos. 
    
    | Restaurante|Tienda de dulces|Panadería|Cafetería|Taverna|Guardería|Hospital|Licorería|Gasolinera|...|
    |:----------|:-------------|:------|:----------|:-------------|:------|:----------|:-------------|:------|:------|
   
    * Risk: Cada establecimiento se clasifica según su riesgo de afectar negativamente a la salud pública.
    
     |Clasificación del riesgo|Descripción|
     |:----|:----|
     |1|Alto|  
     |2|Medio| 
     |3|Bajo|
     |All|Todos| 
     
       La frecuencia de inspección está ligada a este riesgo, siendo los establecimientos de riesgo 1 inspeccionados con mayor frecuencia y los de riesgo 3 con      menor frecuencia, la mayoría de las inspecciones tienen riesgo alto.
 
    * Address: Dirección del establecimiento 
    
    * City: Ciudad estadounidense a la que pertenece el establecimiento, la ciudad que más inspecciones tiene es Chicago.
    
    * State: Estado al que pertenece el establecimiento, la mayoría de las inspecciones se realizarón en el estado de Illinois, y con un registro en el estado de Nueva York, un registro en el estado de Indiana y un registro en el estado de Wisconsin.
    
    * Zip: Código postal del establecimiento.
    
    * Inspection Date: Fecha en la que se realizó la inspección, registros desde el 4 de enero del 2010 hasta el 15 de enero del 2021.
    
    * Inspection Type: Tipo de inspección, existen 110 tipos de inspección.
    
     |Tipo de inspección|Descripción|
     |:----|:----|
     |Sondeo|El tipo de inspección más común que se realiza con una frecuencia relativa al riesgo del establecimiento|
     |Consulta| Cuando la inspección se realiza a solicitud del propietario antes de la apertura del establecimiento|
     |Denuncia|Cuando la inspección se realiza en respuesta a una denuncia contra el establecimiento|
     |Licencia|Cuando la inspección se realiza como requisito para que el establecimiento reciba su licencia para operar|
     |Sospecha de intoxicación alimentaria|Cuando la inspección se realiza en respuesta a una o más personas que afirman haberse enfermado como consecuencia de comer en el establecimiento|
     |Inspección del grupo de trabajo|Cuando se realiza una inspección de un bar o taberna. Pueden producirse reinspecciones para la mayoría de estos tipos de inspecciones y se indican como tales|
     |...|...|

    * Results: Resultado de la inspección
    
     |Resultado|Descripción|
     |:---|:---|
     |Pass|Establecimientos que no tenían violaciones críticas o graves. La mayoría de los establecimientos pasaron la inspección|
     |Fail|Establecimientos que tenían violaciones críticas o graves que no se pudieron corregir durante la inspección. Un establecimiento que recibe una "falla"  no significa necesariamente que la licencia del establecimiento esté suspendida.| 
     |Pass w/ Conditions|Establecimientos que tenían violaciones críticas o graves, pero estas se corrigieron durante la inspección|
     |Out of Business|Establecimientos que se encuentran fuera de servicio|
     |No Entry|Establecimientos a los que no se pudieron entrar para realizar la inspección ¨|
     |Not Ready|Establecimientos cuyo resultado no está definido ¨|
     |Business Not Located|Establecimientos no ubicados|
     
     ¨ Suposición del equipo
    
    * Violations: Un establecimiento puede recibir una o más de 45 infracciones distintas. Para cada número de infracción enumerado para un establecimiento determinado, se indica el requisito que el establecimiento debe cumplir para que No reciba una infracción, seguido de una descripción específica de los hallazgos que causaron la emisión de la infracción.
    
     |Infracciones|1-44 y 70|
     |:---|:---|
    
    * Latitude: Coordenada geográfica, latitud del establecimiento.
    
    * Longitude: Coordenada geográfica, longitud del establecimiento.
    
    * Location: Latitud y longitud   
     

* **Pregunta analítica a contestar con el modelo predictivo:** ¿El establecimiento pasará la inspección?


* **Frecuencia de actualización de los datos:** Esta base de datos se actualiza cada viernes 

*Información obtenida de [Chicago data portal](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)*

