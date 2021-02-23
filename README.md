# DPA Food Inspections 2021

* Integrantes del equipo
  * Edgar Bazo
  * Dira Martínez
  * Iván Salgado
  * Ana Torres
  
  
* Datos a utilizar: Inspecciones a restaurantes y otros establecimientos en Chicago, estas inspecciones son realizadas por el personal del Programa de Protección de Alimentos del Departamento de Salud Pública de Chicago. 

  * **Número de registros:** 215,130 al 15 de enero del 2021
  * **Número de columnas:** 17
 
    * Inspection ID: Identificador de la inspección
    
    * DBA Name: 'Doing business as', hace referencia al nombre legal del establecimiento
    
    * AKA Name: Alias del nombre del establecimiento
    
    * License #: Número único asignado al establecimiento por parte del Departamento de Asuntos Comerciales y Protección al Consumidor. 
    
    * Facility Type: Tipo de establecimiento, 500 diferentes tipos de establecimientos. 
    
         | Restaurante|Tienda de dulces|Panadería|Cafetería|...|
         |:----------:|:-------------:|:------:|:----------:|:------:|
   
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
        |Fail|Establecimientos que tenían violaciones críticas o graves que no se pudieron corregir durante la inspección. Un establecimiento que recibe una falla no significa necesariamente que la licencia del establecimiento esté suspendida.| 
        |Pass w/ Conditions|Establecimientos que tenían violaciones críticas o graves, pero estas se corrigieron durante la inspección|
        |Out of Business|Establecimientos que se encuentran fuera de servicio|
        |No Entry|Establecimientos a los que no se pudieron entrar para realizar la inspección ^|
        |Not Ready|Establecimientos cuyo resultado no está definido ^|
        |Business Not Located|Establecimientos no ubicados|
     
        ^ Suposición del equipo
    
    * Violations: Un establecimiento puede recibir una o más de 45 infracciones distintas. Para cada número de infracción enumerado para un establecimiento determinado, se indica el requisito que el establecimiento debe cumplir para que No reciba una infracción, seguido de una descripción específica de los hallazgos que causaron la emisión de la infracción.
    
        |Infracciones|1-44 y 70|
        |:---:|:---:|
    
    * Latitude: Coordenada geográfica, latitud del establecimiento.
    
    * Longitude: Coordenada geográfica, longitud del establecimiento.
    
    * Location: Latitud y longitud   
     

* **Pregunta analítica a contestar con el modelo predictivo:** ¿El establecimiento pasará la inspección?


* **Frecuencia de actualización de los datos:** Esta base de datos se actualiza diariamente 


* **Dueño de los datos:** Chicago Department of Public Health

   *Información obtenida de [Chicago data portal](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)*


* **Infraestructura del proyecto:**
 
   * Se estará utilizando un entorno virtual _pyenv virtual env_ con la versión de Python 3.7.4
   * Las librerías y sus dependencias que se utilizarán para este proyecto se encuentran en el archivo requirements.txt 
   * EL EDA/GDA de los datos se encuentra en la ruta `notebooks/eda.ipynb`, para poder reproducir este notebook se requiere cargar el script `src/utils/utils_notebook/utils_eda.py` y para reproducir la gráfica del mapa de Chicago se deberán de cargar los archivos que se encuentran en la ruta `notebooks/Boundaries - City`
   * En la [wiki](https://github.com/AnaTorresR/DPA-food_inspections/wiki/Bit%C3%A1cora) encontrarás una bitácora de las acciones realizadas en cada checkpoint, así como su fecha de entrega.
 
* **Proceso de ingesta:** 

 Para poder realizar la ingesta de datos, tanto histórica como semanal, se deberá solicitar un token en la [API](https://dev.socrata.com/foundry/data.cityofchicago.org/4ijn-s7e5), una vez obtenido el token este se deberá de guardar en la ruta `conf/local/credentials.yaml`, así como tus credenciales de aws para poder acceder a tu bucket s3, este archivo *credentials.yaml* debe ser creado de la siguiente manera: 
 
     ---
     s3: 
      aws_access_key_id: "tu-access-key-id"
      aws_secret_access_key: "tu-secret-acces-key"
     food_inspections:
      api_token: "tu-token"
      
También necesitarás el script `src/utils/constants.py` el cual contiene las siguientes constantes: 

    bucket_name = "nombre-de-tu-bucket"
    dataset_domain = "data.cityofchicago.org"
    dataset_id = "4ijn-s7e5"
    
En nuestro caso el bucket que ocuparemos lleva el nombre de *'data-product-architecture-equipo-6'*, en tu caso deberás cambiar la constante *bucket_name* al nombre de tu bucket.

Para correr las funciones **ingesta_inicial** e **ingesta_consecutiva** ubicadas en la ruta `src/pipeline/ingesta_almacenamiento.py` deberás tener tu ambiente virtual activado `pyenv activate tu-ambiente-virtual`, una vez activado tu ambiente deberás ejecutar en la raíz de este proyecto el comando `export PYTHONPATH=$PWD` para que puedas importar las funciones que se encuentran el la carpeta *src/pipeline/ingesta_almacenamiento* y *src/utils/general* y finalmente, mediante un script python (en la raíz de este proyecto) deberás ejecutar las siguientes funciones: 

   - para ingesta_inicial:
  
          from src.pipeline.ingesta_almacenamiento import *
          from src.utils.general import * 
          
          creds = get_api_token('conf/local/credentials.yaml')
          client = get_client(creds['api_token'])
          ingesta_inicial(client)
          
Esta función obtiene los registros históricos que existen hasta el momento de su ejecución y serán guardados como objeto pickle en la ruta `ingestion/initial/historic-inspections-aaaa-mm-dd.pkl` en tu bucket s3. 
     
   - para ingesta_consecutiva: 
   
          from src.pipeline.ingesta_almacenamiento import *
          from src.utils.general import * 
          
          creds = get_api_token('conf/local/credentials.yaml')
          client = get_client( creds['api_token'])
          limit = 1000
          ingesta_consecutiva(client, limit)
          
Esta función se estará ejecutando semanalmente, tomará la fecha del día de ejecución (t) y se le restarán 7 días, lo cual extraerá los registros al tiempo 
(t-1) y serán guardados como objeto pickle en la ruta `ingestion/consecutive/consecutive-inspections-aaaa-mm-dd.pkl` en tu bucket. **Esto es debido a la forma de actualización de los datos que es a día vencido**
  
Para que estas funcionas sean ejecutables se necesita del script `src/utils/general.py` que contiene las funciones `read_yaml`, `get_s3_credentials()` y `get_api_token` que a su vez importa el archivo `conf/local/credentials.yaml` cuya estructura ha sido mencionada anteriormente. 

**OJO:** Asegúrate de haber instalado la versión actual del requirements.txt de la siguiente manera: `pip install -r requirements.txt` dentro de tu pyenv.
