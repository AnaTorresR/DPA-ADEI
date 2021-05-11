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

 **OJO:** Antes de correr cualquier comando asegúrate de haber instalado la versión actual del requirements.txt de la siguiente manera: `pip install -r requirements.txt` dentro de tu pyenv del proyecto.
 
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
    initial_path = "ingestion/initial/historic-inspections"
    concecutive_path = "ingestion/consecutive/consecutive-inspections"
    dataset_domain = "data.cityofchicago.org"
    dataset_id = "4ijn-s7e5"
    
En nuestro caso el bucket que ocuparemos lleva el nombre de *'data-product-architecture-equipo-6'*, en tu caso deberás cambiar la constante *bucket_name* al nombre de tu bucket.

Para correr las funciones **ingesta_inicial** e **ingesta_consecutiva** ubicadas en la ruta `src/pipeline/ingesta_almacenamiento.py` deberás tener tu ambiente virtual activado `pyenv activate tu-ambiente-virtual`. 

Una vez activado tu ambiente deberás ejecutar en la raíz de este proyecto el comando `export PYTHONPATH=$PWD` esto es para que puedas importar las funciones que se encuentran el la carpeta *src/pipeline/ingesta_almacenamiento* y *src/utils/general*. 

Finalmente, mediante un script python (en la raíz de este proyecto) deberás ejecutar las siguientes funciones: 

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

* **Aequitas**

Este proyecto será considerado **asistivo**, debido a que los dueños de los establecimientos podrán observar a través de nuestra API (lista para el 25 de mayo) si su establecimiento pasará o no la inspección, por lo que podrán tomar las medidas necesarias para que el establecimiento pase la inspección el día que se les asigne. 

Los grupos de referencia son los siguientes:

 |Variable|Grupo|
 |:---:|:---:|
 |Tipo de establecimiento|Restaurante|
 |Riesgo| 1. Alto |
 | Tipo de inspección|Canvass|

La razón por la que seleccionaos estos grupos de referencia es porque son las categorías con la mayor frecuencia en nuestros datos. Lo puedes ver nuestro [EDA](https://github.com/AnaTorresR/DPA-food_inspections/blob/main/notebooks/eda.ipynb)

Las métricas consideradas en este proyecto serán:

|FNR| Nos interesa saber si los establecimientos que pasaron la inspección cuántas de esas veces nos equivocamos en la predicción debido al tipo de establecimiento.|
|FOR| Nos interesa conocer si hay un sesgo hacia algún grupo de no ser seleccionado como etiqueta positiva.|
|TPR | Tasa de verdaderos positivos |


* **LUIGI:** 

 Se crearon dos módulos llamados _ingesta_task.py_, _almacenamiento_task.py_ ubicados en la paquetería `src/pipeline`. Estos módulos contienen las task llamadas _IngestaTask_ y _AlmacenamientoTask_ respectivamente. 
 
 _ingesta_task.py_: Obtiene los datos de la API de Food Inspections y son guardados de manera local en formato .pkl. Estos datos son guardados de manera local en formato .pkl en la siguiente ruta `temp/data-product-architecture-equipo-6/ingestion/ 'la ingesta que corriste'/ 'la ingesta que corriste'-inspections-aaaa-mm-dd.pkl`. Esta carpeta es generada de manera automática por este task. 
 
 _almacenamiento_task.py_: Guarda el .pkl generado en el task anterior en tu bucket s3.
 
 En una terminal activa tu pyenv y ejecuta el comando `luigid`, posteriormente en tu navegador escribe lo siguiente `localhost:8082`, así podrás ver la DAG de tus tasks.
 
 En otra terminal, para poder ejecutar estos tasks deberás ubicarte en la raíz de este proyecto y ejecutar el siguiente comando con tu pyenv activado:
 
 __Ingesta histórica:__
 
      PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_task AlmacenamientoTask --ingesta historica --year aaaa --month mm --day dd
 
 __Ingesta consecutiva:__
 
    PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_task AlmacenamientoTask --ingesta consecutiva --year aaaa --month mm --day dd
    
Si es la primera vez que ejecutas la ingesta histórica/consecutiva deberás indicar la fecha en la que estás ejecutando este task.

Si únicamente deseas comprobar que tu ingesta histórica/consecutiva se encuentra en tu bucket s3 deberás indicar la fecha con la que se encuentra guardada esta ingesta.
     
__------------->__ Por la forma en la que está construida la task de ingesta consecutiva, para evitar la duplicación u omisión de observaciones. Se debe ejecutar cada 7 días a la misma hora, o si es la primera consecutiva, 7 días después de la histórica.      
  
 * **RDS:**
 
 Para continuar con los siguientes pasos del proyecto es necesario contar con una base de datos destinada para el proyecto en una RDS de PostgreSQL. Ten en cuenta que para esto deberás de tener instalado psql en tu computadora. Si no lo tienes instalado, puedes instalarlo copiando y pegando lo siguiente en tu terminal:
 
                sudo apt install postgresql postgresql-contrib
 
 Una vez que tengas tu RDS, al archivo `credentials.yaml` que creamos anteriormente, es necesario agregarle también las credenciales de nuestra base de datos debajo de las credenciales anteriores, agrégalas de la siguiente manera:

    db:
     user: "nombre-de-tu-usuario"
     pass: "contraseña-de-tu-usuario"
     host: "url-de-tu-base-de-datos"
     port: "5432"
     db: "nombre-de-tu-base-de-datos"
  
  Además, deberás de crear el archivo `.pg_service.conf` en el `/home` con las siguientes líneas:
          
     [food]
     user=postgres
     password=aquí-tu-contraseña
     host=endpoint-de-tu-rds
     dbname=aquí-el-nombre-de-tu-base
     port=5432
  
  En el directorio ![sql/](https://github.com/AnaTorresR/DPA-food_inspections/tree/main/sql) se encuentran los scripts `create_clean_table.sql`, `create_metadata_table.sql`, `create_semantic_table.sql` y `create_tests_table.sql` para crear sus correspondientes tablas en PostgreSQL. Para correr estos scripts deberás posicionarte en la raíz del repositorio y ejecutar el siguiente comando en tu terminal:
  
  ```
  psql -f sql/create_clean_table.sql service=food
  psql -f sql/create_metadata_table.sql service=food
  psql -f sql/create_semantic_table.sql service=food
  psql -f sql/create_tests_table.sql service=food
  ```
  
  O puedes copiar y pegar el contenido de los scripts dentro de tu base de datos. Recuerda que para conectarte a tu base de datos debes correr:
  
     psql -h url-de-tu-rds -U postgres -d nombre-de-tu-base-de-datos
  
  o bien, usando tu pgservice:
      
      psql service=food
     
  Para ver el contenido de cualquier tabla puedes ejecutar lo siguiente desde postgres:
  
        select * from <esquema>.<tabla>;
  
 * **Preprocessing:**
 
 A partir de ahora, para todos las task que realicemos en el pipeline del proyecto se generará la metadata relevante asoaciada a cada una de las tasks. Esto incluye a las tasks de ingesta y almacenamiento que habíamos realizado antes.
 
 En `src/pipeline` se crearon seis modulos relacionados con el preprocesamiento de los datos y la creación de metadata:

 + _cleaning_task.py_ : Contiene el task _CleaningTask_ que lee los datos resultantes del proceso de ingesta del bucket de s3, les hace una serie de transformaciones de limpieza y finalmente, sube los datos limpios a la base de datos a la tabla de `features` dentro del esquema `clean`.
 + _feature_engineering_task.py_ : Incluye la task _FETask_ la cual lee los datos limpios de `clean.features` y realiza las transformaciones necesarias para la ingeniería de características para después subir los datos transformados a la tabla `features` del esquema `semantic`.
 + _ingesta_metadata_task.py_, _almacenamiento_metadata_task.py_, _cleaning_metadata_task.py_, _feature_engineering_metadata_task.py_ : Estos módulos incluyen las tasks de _IngestaMetadataTask_, _AlmacenamientoMetadataTask_, _CleaningMetadataTask_, _FEMetadataTask_ respectivamente. Estas task se encargan de escribir la metadata relevante de cada una de sus correspondientes tareas en la tabla de `metadata` en la base de datos. Esta metadata relevante incluye: tipo de task, tipo de ingesta, fecha de ejecución y autor.

 Para correr los tasks anteriores con LUIGI, en una terminal activa tu pyenv y ejecuta el comando `luigid`, posteriormente en tu navegador escribe lo siguiente `localhost:8082`, así podrás ver la DAG de tus tasks. O, si lo estás corriendo desde tu bastión, realiza un port fordwarding de la siguiente manera:
 
      ssh -i ~/.ssh/id_rsa -NL localhost:<puerto-libre-en-tu-computadora>:localhost:8082 tu-usuario@url-de-tu-bastion
      
 Y abre la interfaz de luigi escribiendo `localhost:<puerto-libre-en-tu-computadora>` en tu navegador.
 
 En otra terminal, para poder ejecutar estos tasks deberás ubicarte en la raíz de este proyecto y ejecutar el siguiente comando con tu pyenv activado:
 
 __Limpieza:__
 
      PYTHONPATH='.' luigi --module src.pipeline.cleaning_task CleaningTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd
 
 __Feature Engineering:__
 
      PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_task FETask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd
      
 __Metadata Ingesta:__
 
      PYTHONPATH='.' luigi --module src.pipeline.ingesta_metadata_task IngestaMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd
      
 __Metadata Almacenamiento:__
 
      PYTHONPATH='.' luigi --module src.pipeline.almacenamiento_metadata_task AlmacenamientoMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd
      
 __Metadata Limpieza:__
 
      PYTHONPATH='.' luigi --module src.pipeline.cleaning_metadata_task CleaningMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd
      
 __Metadata Feature Engineering:__
 
      PYTHONPATH='.' luigi --module src.pipeline.feature_engineering_metadata_task FEMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd

__Entrenamiento:__
   
    PYTHONPATH='.' luigi --module src.pipeline.entrenamiento_task EntrenamientoTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd 

__Metadata Entrenamiento:__

    PYTHONPATH='.' luigi --module src.pipeline.entrenamiento_metadata_task EntrenamientoMetadataTask --ingesta <tipo-de-ingesta>  --year aaaa --month mm --day dd 

__Selección Modelo:__

    PYTHONPATH='.' luigi --module src.pipeline.seleccion_modelo_task SeleccionModeloTask --ingesta <tipo-de-ingesta>  --year aaaa --month mm --day dd 

__Metadata Selección Modelo:__

    PYTHONPATH='.' luigi --module src.pipeline.seleccion_modelo_metadata_task SeleccionModeloMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd 
    
__Aequitas:__

    PYTHONPATH='.' luigi --module src.pipeline.aequitas_task AequitasTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd --model-type 'assistive'
    
O puedes omitir el parámetro `model-type` pues nuestro pipeline tiene el valor _assistive_ por default.
    
__Metadata Aequitas:__ 
       
    PYTHONPATH='.' luigi --module src.pipeline.aequitas_metadata_task AequitasMetadataTask --ingesta <tipo-de-ingesta> --year aaaa --month mm --day dd --model-type 'assistive'

* **Pruebas Unitarias**

Se crearon pruebas unitarias enfocadas a los datos para cada una de las tareas del pipeline. Estas pruebas tienen el objetivo de verificar la integridad de los datos que ingestamos y que estos sean congruentes con los datos anteriores, para asegurar que si alguna tarea falla no sea por los datos si no por la estructura de nuestros pipelines. Estas pruebas unitarias también fallan si se intenta ingestar con una fecha futura. 

+ Test Ingesta y Test Almacenamiento:
     + Verifica si existe el archivo guardado en la carpeta temporal `temp`.
     + Verifica si existen los 4 tipos de riesgos en los datos ingestados.
     + Verifica que la variable `inspection_date` tenga fechas coherentes.
     + Verifica que el archivo guardado en la carpeta temporal no esté vacío.
     + Verifica que se esté realizando ingesta de datos de fechas ya ocurridas.

* Test Cleaning:
     + Verifica que todos los registros estén en minúsculas.
     + Verifica que el número de columnas sean exactamente 16.
     + Verifica que se esté realizando ingesta de datos de fechas ya ocurridas.
               
* Test Feature Engineering y Entrenamiento:
     + Verifica que los datos tengan más de una columna.
     + Verifica que los datos tengam más de un registro.
     + Verifica que se esté realizando ingesta de datos de fechas ya ocurridas.
 
* Test Selección Modelo:
     + Verifica que el tamaño del archivo guardado como el mejor modelo en el bucket S3 sea mayor a 0 bytes.
     + Verifica que se esté realizando ingesta de datos de fechas ya ocurridas.

* Test Aequitas:
     + Verifica que el análisis de sesgo e inequidad se realice para 3 tipos de atributos (facility_type, risk e inspection_type)
     + Verifica que la tabla resultante contenga 4 métricas para cada grupo ('for_disparity', 'fnr_disparity', 'tpr_disparity','fnr_disparity')
     + Verifica que la tabla resultante no esté vacía.
     + Verifica que sólo se realice el análisis para fechas ya ocurridas.
     + Verifica que el modelo sea de tipo asisitivo con el parámetro ``model-type``.

 * **DAG**
 
  ![DAG](img/checkpoint_6.jpg)
