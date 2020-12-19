PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/pluginfile.php/3145524/mod_assign/introattachment/0/spk_8mu.tgz?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

  El pipeline principal en el script `wav2lp.sh` es el siguiente:
  ```
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
    $LPC -l 240 -m $lpc_order > $base.lp
  ```
  donde $X2X, $FRAME, $LPC se sustituyen por "sptk x2x", "sptk frame" y "sptk lpc" respectivamente; 
  $inputfile y $lpc_order se sustituyen por el nombre del archivo de entrada y el orden del predictor que se 
  especifique; y $base se sustituye por el nombre correspondiente para los archivos temporales.

  Los comandos involucrados realizan las siguientes funciones:

  * sox: Programa capaz de leer, escribir y manipular archivos de audio en la mayoría de los formatos usuales. 
  Las opciones que se han empleado son:
  `-t raw` que indica el tipo de archivo de audio. Lo añadimos para informar al programa sox que se trata de un 
  arxivo de audio sin cabecera.
  `-e` que indica el tipo de codificación de audio. Usamos `signed` para pasarlo a real. 
  `-b 16` para indicar que queresmos que sea de 16 bits.

  Programas de SPTK:

  * x2x: Convierte los datos de una entrada estándar (generalmente el teclado) a otro tipo y los saca por la salida 
  estándar (generalmente por pantalla). 
  La opción empleada es la de `+sf` formada por "+", el tipo de datos de entrada (s: short) y el tipo de datos de 
  salida (f: float).

  * frame: Convierte una secuencia de datos de entrada en una serie de tramas posiblemente solapadas de periodo 
  longitud l y periodo p, y lo saca por la salida estándar. En este caso, se están creando tramas de 240 muestras 
  de longitud (30 ms) y 80 muestras de periodo (10 ms) (desplazamiento de ventana) utilizando las opciones `-l 240 -p 80`
  (En esta práctica la frecuencia de mostreo es de 8 kHz). 

  * window: Multiplica elemento a elemento los vectores de un archivo de entrada (o la entrada estándar) por una 
  función de ventana específica, enviando el resultado a la salida estándar. En este caso se usan las opciones 
  `-l 240 -L 240` indicando la longitud de las tramas de entrada y salida respectivamente. Al no indicar la ventana 
  con la opción `-w`, se utiliza la definida por defecto, que es la ventana de Blackman.     

  * lpc: Calcula los coeficientes de predicción lineal. Para ello, se le indica la longitud de la ventana de 
  datos con la opción `-l 240` (en esta caso 240 muestras) y `-m` para indicar el orden del predictor.     


- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).

  Las líneas a analizar son las siguientes:
  ```
  # Our array files need a header with the number of cols and rows:
  ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
  nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'`
  ```

  Para obtener un fichero de formato *fmatrix*, queremos almacenar los datos en nrow filas de ncol columnas, en los que cada fila corresponda a una trama de señal, y cada columna a cada uno de los coeficientes con los que se parametriza la trama. Por tanto, este fichero debe indicar el número de filas y columnas al principio del fichero. Posteriormente se escribirán los datos como reales de 4 bytes (formato float de C). 

  El número de columnas se calcula a partir del orden del predictor (orden del predictor + 1):
  ```
  ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
  ```

  El número de filas se obtiene de la siguiente forma: Primero, se convierte la señal parametrizada del propio fichero obtenido a texto, usando el conversor de SPTK x2x con la opción +fa (de float a ASCII). Luego se utiliza el comando de UNIX wc (word count) con la opción -l para contar las filas. Finalmente, el comando perl es el intérprete para el lenguaje de programación Perl. La *e* se usa para introducir una línea de código y la *n* para que repita la acción en bucle. Por tanto, `perl -ne 'print $_/'$ncol', "\n";'` introduce repetidamente dicha línea de código. Esto se hace porque wc -l no cuenta la última línea si no contiene `\n`.   

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.

  Es conveniente usar este formato para poder usar los programas fmatrix_show y fmatrix_cut que nos permiten mostrar el contenido de estos ficheros o seleccionar columnas concretas de los mismos, además de que permite almacenar los datos como reales de 4 bytes (float) en vez de formato texto (ASCII).  


- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
```
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	$LPC -l 240 -m $lpc_order | $LPC2C -m $lpc_order -M $cepstrum_order > $base.lpcc
``` 


- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
```
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	$MFCC -l 240 -m $mfcc_order -n $mfcc_order_ch -s 8 -w 1 > $base.mfcc
```


### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.

  ![LP](/IMG/LP.PNG)
  ![LPCC](/IMG/LPCC.PNG)
  ![MFCC](/IMG/MFCC.PNG)
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    
    LP
    ```
    fmatrix_show work/lp/BLOCK01/SES017/.lp | egrep '^[' | cut -f4,5 > lp_2_3.txt
    ```
    LPCC
    ```
    fmatrix_show work/lpcc/BLOCK01/SES017/.lpcc | egrep '^[' | cut -f4,5 > lpcc_2_3.txt
    ```
    MFCC
    ```
    fmatrix_show work/mfcc/BLOCK01/SES017/*.mfcc | egrep '^[' | cut -f4,5 > mfcc_2_3.txt
    ```

    Con estos comandos copiamos los resultados de las parametrizaciones en unos archivos .txt con dos columnas, una de coeficientes 2 y la otra de coeficientes 3. Con estos archivo y mediante MATLAB graficaremos estos datos con la función scater(). Este es el código de MATLAB:

    ```
    LP_file = fopen('C:\Users\marcb\Downloads\lp_2_3.txt','r');
    LPCC_file = fopen('C:\Users\marcb\Downloads\lpcc_2_3.txt','r');
    MFCC_file = fopen('C:\Users\marcb\Downloads\mfcc_2_3.txt','r');

    formatSpec = '%f %f';
    sizeA = [2 Inf];
    sz = 2;

    LP = fscanf(LP_file,formatSpec,sizeA);
    LPCC = fscanf(LPCC_file,formatSpec,sizeA);
    MFCC = fscanf(MFCC_file,formatSpec,sizeA);

    fclose(LP_file);
    fclose(LPCC_file);
    fclose(MFCC_file);

    LP = LP';
    LPCC = LPCC';
    MFCC = MFCC';

    figure
    scatter(LP(:,1), LP(:,2), sz,'filled', 'black');
    title('LP');
    figure
    scatter(LPCC(:,1), LPCC(:,2), sz,'filled', 'black');
    title('LPCC');
    figure
    scatter(MFCC(:,1), MFCC(:,2), sz,'filled', 'black');
    title('MFCC');
    ```

  + ¿Cuál de ellas le parece que contiene más información?

   La correlación indica lo mucho que se parecen los parametros, por lo tanto la información será inferior cuanto más alta sea la correlación. La parametrización MFCC es la más incorrelada y, por tanto, la que contiene más información. Después de está esta la LPCC que aporta más información que la LP pero menos que la MFCC. 

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] | -0.873681 | 0.184235 | -0.11304 |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
  |&rho;<sub>x</sub>| -> 1  (correlación alta)      |&rho;<sub>x</sub>| -> 0  (correlación baja)

  Se puede ver que los datos coinciden con las gráficas anteriores. En el caso de LP, se aproxima a 1, por lo que están bastante correladas y aporta poca información. En los casos de LPCC y MFCC, se aproximan a 0, por lo que están más incorreladas y aportan más información, siendo MFCC la que más información aprota.

- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

 Según la teoría de LPCC, [Q = (3/2)*p], siendo la "p" el orden y la "Q" son los coeficientes de cepstrales. Nosostros hemos escogido p = 14 y Q = 21. En el caso de la parametrización MFCC, el orden es Q = 13 y el número de filtros es M, que está entre 24 y 40. Nosotros hemos escogido Q = 13 y M = 35.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

  ![gmm](/IMG/gmm1.PNG)
  
- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

  ![GMM_SES098_013](/IMG/GMM_SES098_013.PNG)

  Tenemos las regiones del 50% y 90% de la masa de probabilidad de GMM. El color rojo corresponde al locutor SES098 y el azul al SES013. En estas cuatro imagenes se muestran los dos locutores con el GMM correspondiente y intercambiado. Cueando está intercambiado, es decir, la población y el locutor no coinciden, las regiones no encajan con la poblacion. Cuando el locutor y la población coinciden, las regiones encajan perfectamente.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  |     Tasa de error      | 7.77 % | 1.40 % | 0.76 % |

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
  |                 | LP | LPCC | MFCC |
  |-----------------|:----:|:----:|:----:|
  | THR             | 1.548618 | 0.679109 | 0.830055 |
  | Missed          | 225/250 = 0.9 | 61/250 = 0.2440 | 71/250 = 0.2840 |
  | False Alarm     | 0/1000 = 0 | 1/1000 = 0.0010 | 0/1000 = 0|
  | Cost Detection  | 90.0 | 34.3 | 28.4 |

### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
