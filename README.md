# DPA Food Inspections 2021

* Integrantes del equipo
  * Edgar Bazo
  * Dira Martínez
  * Iván Salgado
  * Ana Torres
  
  
* Datos a utilizar: Inspecciones a restaurantes y otros establecimientos en Chicago, estos datos fueron obtenidos de la siguiente [página](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)
  * **Número de registros:** 215,000 al 17 de enero del 2021
  * **Número de columnas:** 17
    * Inspection ID: Identificador
    * DBA Name: Nombre del establecimiento 
    * AKA Name: Alias del establecimiento
    * License #: Licencia del establecimiento 
    * Facility Type: Tipo de establecimiento, 500 diferentes tipos de establecimientos 
    * Risk: Riesgo de no pasar la inspección 1: Alto, 2: Medio, 3: Bajo, Todos. La mayoría de las inspecciones tienen riesgo alto.
    * Address: Dirección del establecimiento 
    * City: Ciudad estadounidense a la que pertenece el establecimiento. 
    * State: Estado al que pertenece el establecimiento, la mayoría de las inspecciones se realizarón en el estado de Illinois, y con un registro en el estado de Nueva York, un registro en el estado de Indiana y un registro en el estado de Wisconsin.
    * Zip: Código postal
    * Inspection Date: Fecha en la que se realizó la inspección, registros desde enero del 2010 con actualizaciones diarias.
    * Inspection Type: Tipo de inspección, existen 110 tipos de inspección, de los cuales la mayoría están clasificadas como' Canvass' = Sondeo.
    * Results: Resultado de la inspección: Pass, Fail, Pass w/ Conditions, Out of Business, No Entry, Not Ready, Business Not Located; la mayoría de los establecimientos pasaron la inspección. 
    * Violations: Tipo de violaciones, existen 65 tipos de violaciones, la mayoría de los registros no cuentan con descripción en este campo.
    * Latitude: Coordenada geográfica, latitud del establecimiento.
    * Longitude: Coordenada geográfica, longitud del establecimiento.
    * Location: Latitud y longitud en Estados Unidos.  
     

* **Pregunta analítica a contestar con el modelo predictivo:** ¿El establecimiento pasará la inspección?


* **Frecuencia de actualización de los datos:** Esta base de datos se actualiza de manera diaria, sin embargo, para este proyecto los datos se estarán actualizando de manera semanal. 
