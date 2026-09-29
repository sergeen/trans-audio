# Transcripción Completa: Artistas que Hacen Software
**Evento:** PREMAC — Centro Cultural de la UNC (Córdoba, Argentina)  
**Fecha:** 22 de Septiembre de 2026  
**Captura:** Sistema de transcripción en tiempo real con IA local [`trans-audio`](README.md) (*sherpa-onnx*)

### Panelistas:
- **Sergio Scotta**: Moderador, artista y programador. Creador del mapeo relacional de actores e instituciones del arte.
- **Constanza Chiappini (Coty)**: Artista visual. Creadora de [**Vapor**], plataforma web para portfolios de artistas sin intermediación algorítmica.
- **Lola Granillo**: Artista. Creadora de [**Gotla**], plataforma sobre OpenStreetMap para geolocalización de eventos y talleres artísticos.
- **Electrosoma**: Colectivo musical de Electronic Body Music (EBM).
- **Asistente del Público**: Aporte sobre asambleas, cooperativismo y la economía de los dones.

---


## 1. Apertura, prueba de sonido y contexto del encuentro

**[00:00] Sergio Scotta:**
A ver si ahora nos entendemos... Después voy a revisar el dato. Hello... Ya lo vamos a recuperar. Solo estática está recibiendo. Bueno.

**[00:40] Sergio Scotta:**
¿Lo arrancamos? Bueno, vamos a arrancarlo, gente, así no se nos mueren de hipotermia. Y vamos a dejarlo de fondito aunque esté andando más o menos. Bueno, sí, ahora que nos ilumine el objetivo ahí.

Bueno, gente, vamos a darle comienzo un poquito a esto para que no nos dé tanto frío, porque se está poniendo muy fresco. Bueno, y ¡Dios Santo estos días soleados!

Primero, gracias a todos los que se han acercado para acá. Si está intentando... ¡ah, mira, ahí los está tomando! Algunas de las cosas... Bueno, eso que estamos viendo ahí en pantalla es un sistema de inteligencia artificial que va a ir registrando todo lo que decimos, así nos queda para la próxima, un registro, o para subirlo. Para las próximas generaciones, si quieren acceder a esto de alguna forma.

Bueno, esta charla es en el contexto del PREMAC [Centro Cultural de la UNC]. La estamos haciendo invitando a artistas a que nos cuenten cosas que están haciendo, y en este caso en particular vamos a estar hablando un poquito de artistas que hacen software. No vamos a estar hablando de arte hecho *con* inteligencia artificial o con software, sino de artistas que están utilizando herramientas —algunas de inteligencia artificial y otras más convencionales, como trabajar en equipo— para hacer herramientas de software. Vamos a hablar un poquito sobre lo que está pasando con esto y algunas preguntas que nos está abriendo.

Acá Constanza Chiappini, artista de Córdoba que ahora reside en Buenos Aires, nos va a estar presentando una aplicación que se llama **Vapor**, que es un portfolio para artistas. Lola Granillo nos va a estar hablando de que ella está trabajando con otros desarrolladores haciendo una aplicación de geolocalización de eventos del mundo del arte [**Gotla**]. Y acá yo estoy en este momento dedicado principalmente al arte, vengo del mundo de la programación y el diseño, y les voy a estar mostrando también un proyecto que estoy comenzando para analizar relaciones entre diferentes actores e instituciones del mundo del arte.

También anda dando vueltas el grupo **Electrosoma**, que nos va a estar musicalizando un ratito. Nos van a traer un género que se llama EBM, estamos intentando construir una pequeña escena de eso en Córdoba y cada tanto hacemos eventos, así que vayan porque están buenos.

Voy a sacar esto de pantalla. Si te parece Lola, arrancamos con vos, ¿tenés ganas?


## 2. Gotla: Geolocalización de eventos artísticos sin algoritmos (Lola Granillo)

**[03:58] Sergio Scotta:**
Bueno, lo primero que vamos a hacer es ver la aplicación. Esto es lo que estabas trabajando, ¿no es cierto? Tenemos solamente dos micrófonos, así que sí, divinamente. Bueno, esta es una versión que probablemente después subamos, ¿no es cierto? Bueno, ahí estamos nosotros y ahí está nuestra charla. Lola, creo que lo primero con lo que vamos a empezar es cuáles fueron las motivaciones para empezar a construir un software, cómo comenzó esto de construir una aplicación y por qué.

**[04:42] Lola Granillo:**
Bien. En el caso de **Gotla**, la motivación es descentralizar un poco de Instagram y todo eso. Es algo básico, más como una cuestión de no aguantar esa forma de compartir y de entrar al teléfono y perderse horas cuando solo querés ir al encuentro de lo que está más o menos cerca o saber qué está pasando. Y hacerlo tan sencillo como eso.

La razón por la que me metí a hacer Gotla no fue ni siquiera por competir con redes sociales, porque es imposible competir con esos espacios, sino por plantear otra posibilidad de ver el mundito que hay alrededor del arte. Mi fantasía un poco era recuperar algo del *Sí o No*, como esas revistas que salían en los 2000 donde entrabas a ver qué pasaba y directamente ibas a esas fiestas, que no eran solo para un circuito de gente amiga o conocidos. Las dinámicas de Facebook e Instagram se volvieron un poco encerradas en mundos desconocidos: tenés que saber que existe tal persona que hace tal cosa, seguirla, estar entrando a ver qué postea, qué enseña, etc. Me parece un poco encerrado.

Pensaba también en mi mamá o en personas que no son usuarias de redes y de repente quieren ir a hacer un taller de pintura, un coro o clases de cualquier cosa. Como de repente nos limitamos a postear únicamente en esos espacios, nunca trasciende nuestros circuitos de cercanía y de seguidores. Entonces es eso, digamos: Gotla.

**[07:03] Sergio Scotta:**
Bueno, ahora estamos haciendo un pequeño recorrido de lo que la aplicación hace. Lo que estamos viendo en pantalla es básicamente un mapa. No están usando Google, están usando **OpenStreetMap**. Eso está interesante porque es una versión open source: la comunidad explica cómo está construida una ciudad y lo suben ahí, en vez de usar una herramienta propietaria como Google Maps que tiene muchas limitaciones y esto ya estaría lleno de propaganda. Claro, sería un mapa lleno de información que no viene al caso. Bueno, y las personas pueden subir sus eventos desde acá, ¿no es cierto?

**[07:44] Lola Granillo:**
Sí, te lo permite desde acá. Es medio espíritu fotologuero. Eso me importaba mucho, porque después vi que hay nuevos mapas con lógicas parecidas pero más institucionales. Yo los veo y veo un montón de información basura, botones por todos lados, burocracia que me aturde la mirada por completo. Quería que no tenga nada: que entres, veas qué hay cerca y en todo caso pinches filtros para sacar lo que no querés o ver qué hay hoy, mañana o en el mes. Que sea muy simple de ver y usar.

Incluso no sé si tenés algún registro hecho, hay una fiesta de rutera... Yo subí muchos eventos desde un usuario de Gotla especialmente para esta charla, para que después lo podamos ver y se entienda que aparecen como puntitos. Pero también hay gente que ya lo usó. Vos, por ejemplo, creo que subiste un evento, ¿no?

**[09:00] Sergio Scotta:**
Sí, y un par más.

**[09:25] Sergio Scotta:**
Lo que digo es que, cuando yo entré a Gotla, me pareció súper fácil de usar, súper intuitivo. Tiene una interfaz súper limpia, súper pulcra: entrás, subís la foto, ponés el título y punto. Te permite navegar y poner un hipervínculo de dónde están las entradas o el perfil de Instagram y ya queda publicado.

**[10:06] Lola Granillo:**
Para mí era importante que se sienta re simple, porque de entrada ya te estás creando otro usuario —cosa que creo que todos estamos podridos de crearnos usuarios y contraseñas—. Pero es medio imposible de evitar por cuestiones de seguridad. Más adelante puede ser desafiante ver cómo este espacio se mantiene cumpliendo esta función y no se vuelve un lugar donde uno entra y postea cualquier cosa espantosa geolocalizada. Pero en principio la idea es que sea simple. Y también el recorrido adentro del escritorio es muy simpático, después lo podemos ver.

**[10:56] Sergio Scotta:**
¿Cuál es el recorrido ese?

**[10:56] Lola Granillo:**
Tendrías que iniciar sesión.

**[11:06] Sergio Scotta:**
Bueno, en general básicamente es una aplicación para ver en un mapa las actividades artísticas cercanas. Esa es la idea básica; después hay muchas más cosas que se pueden hacer, pero la primera para que funcione, se entienda y se empiece a usar es esa. Tiene muchísimas posibilidades, y una de las que vamos a hablar hoy es cómo se pueden conectar entre sí las aplicaciones que vamos a ver hoy.

Le quiero pasar la palabra a Constanza Chiappini. Vamos a echarle una mirada al trabajo que vos venís haciendo.


## 3. Vapor: Portfolios limpios para artistas visuales (Constanza Chiappini)

**[12:01] Sergio Scotta:**
Bueno Coty, ¿cuál es la motivación detrás de tu aplicación y de qué se trata?

**[12:01] Constanza Chiappini (Coty):**
La aplicación se llama **Vapor**. La motivación es muy similar a la de Lola: un hartazgo generalizado en relación a las redes sociales, sobre todo por cómo se han ido desarrollando estos últimos años y cómo han perdido su función original, que justamente era encontrarse y ver qué estaba haciendo cada uno, ver las obras. De repente es un display o una necesidad de hacer un montón de cosas...

Y un poco esa demanda que tiene Instagram de actualización permanente: 'Yo soy un artista, me tengo que estar filmando acá mientras pinto o dibujo'. Hay algo de la práctica artística que se pierde en esa necesidad de mostrarse a sí mismo haciendo algo, cuando en realidad se trata de volver un poco para atrás y decir: *lo que importa es la obra*.

**[13:22] Sergio Scotta:**
¿Qué perfil tenía cosas cargadas, por ejemplo?

**[13:22] Constanza Chiappini (Coty):**
Yo tengo todo cargado en Autobomba. Y Facu Díaz tiene cargado lo de Guille Mena, Ezequiel...

**[13:34] Sergio Scotta:**
Muy bien, hicieron la tarea.

**[13:41] Constanza Chiappini (Coty):**
Hicieron la tarea, tal cual. Uno entiende que las redes sociales no son competencia, pero creo que va a haber una necesidad de migrar en algún momento a plataformas un poco más limpias y menos demandantes del algoritmo.

Yo también lo pensé así como Lola pensó en su mamá: pensé en otra generación un poco más grande que la nuestra, que no son nativos digitales. Hay muchas personas que van a talleres, pintan, dibujan, esculpen y necesitan un espacio, porque son el target predilecto para caer en las redes y entrar en ese bucle donde entrás a Facebook durante tres minutos y ves que todo está hecho con inteligencia artificial. Es un poco retornar a cierta veracidad sobre la práctica artística y una puesta en valor. Combatir eso hasta que termine de pegar la vuelta y volvamos a algo más auténtico.


## 4. Mapeo Relacional de Actores e Instituciones del Arte (Sergio Scotta)

**[14:59] Sergio Scotta:**
Más allá de la obra con inteligencia artificial, les voy a mostrar brevemente un proyecto en el que estoy trabajando. Personalmente tengo una dificultad: me cuesta recordar quién es quién en el mundo del arte y quién hace qué con quién. Aprovechando mis estudios de sociología y conociendo autores que dan pistas sobre cómo construir mapas de bola de nieve (como el proyecto *Bola de Nieve*, un proyecto colaborativo histórico que registraba artistas cordobeses), comencé a construir un mapa relacional.

Básicamente toma datos de la web: los registros están construidos en base a inteligencia artificial que busca fuentes y genera biografías automáticamente. Es una herramienta de investigación, no algo público de momento.

La aplicación construye un mapa de cómo los artistas e instituciones se van relacionando. Obviamente la inteligencia artificial no tiene criterios humanos: extrae patrones estadísticos. Por ejemplo, si busca por 'papel' o 'piel', va a agrupar a todos los artistas en cuyas obras y textos recientes la palabra 'papel' fue muy frecuente. O podemos filtrar institucionalmente por quienes circulan en Argentina y ver las conexiones.

Muchos de estos datos se los he 'robado' [scraped] a Constanza. La inteligencia artificial está habilitando que podamos hacer estas cosas: esta aplicación me llevó aproximadamente 9 horas de trabajo distribuidas en 3 días (4 horas de pensamiento, 3 horas de ejecución de código y un año y medio de tomar notas). Yo la construí como programador, pero ustedes tuvieron procesos muy diferentes.


## 5. Cómo se programaron: IA vs. Desarrollo Humano Tradicional

**[19:44] Sergio Scotta:**
Quiero hacer énfasis en esto: Coty nunca programó en su vida, y en pocos meses tuvo lista y andando la aplicación Vapor.

**[20:04] Constanza Chiappini (Coty):**
Fueron tres meses de trabajo con jornadas de hasta 16 horas, con la prueba y error y la neurosis como principal motor. El primer acercamiento es fabuloso: decís 'mirá todo lo que se puede hacer con IA'. Después viene la parte del criterio y la parte ética: confiar en tu propia ética de trabajo para no dañar a nadie.

De repente era una herramienta que podía manipular. Yo tenía un acercamiento teórico a cómo funciona la programación, pero nunca había accionado sobre ella. Al principio fue fantástico, pero después me di cuenta de que armar el código básico era lo de menos: lo más complejo era la seguridad, la conexión con base de datos, el registro de usuarios y cómo se complejizaba a medida que necesitaba más filtros y reglas.

**[21:44] Sergio Scotta:**
Y conectando con lo tuyo, Lola: contanos cómo produjiste Gotla, cuánto tiempo te llevó y cómo fue tu proceso, que fue mucho más tradicional: buscar gente que colabore.

**[22:11] Lola Granillo:**
Cuando apareció la idea hice unos bocetos bastante parecidos a lo que se ve hoy, pero con otra estética. Salí a buscar plata primero, y apareció Pocho: Pocho puso dinero, es el socio capitalista, y yo puse la otra mitad. Saqué la app en este estado para salir a buscar fondos.

Contacté a una diseñadora gráfica [Delfina] y a un programador [Maxi], que hizo todo de manera súper manual; casi no utilizó inteligencia artificial para nada. Pero claro: llevó **dos años** hacerlo. Dos años también porque no teníamos la plata para pagar una dedicación full time: era 'acá hay doscientos más, a ver cuánto tiempo le podés meter'. No fue por oponernos a la IA, sino porque el programador trabajaba así y yo tampoco tenía tiempo de ponerme a aprender esa herramienta.

**[23:52] Sergio Scotta:**
A mí me parece que trabajar con otras personas tiene algo muy nutritivo: la fricción te va trayendo cosas nuevas.

**[24:12] Lola Granillo:**
Totalmente, hubo muchas idas y vueltas. Muchas ideas originales mejoraron muchísimo hablándolas tanto con Maxi, el programador, como con Delfina, la diseñadora.


## 6. El gran desafío: Adquisición de usuarios, barreras y modelos de sostenibilidad

**[24:23] Sergio Scotta:**
Además de las dificultades técnicas, creo que hay una dificultad principal: la participación de la gente. Cuando creás un producto de este tipo, ¿cómo llevan adelante esa dificultad de que la gente lo use?

**[24:43] Lola Granillo:**
Cuesta usar algo nuevo porque ya tenés demasiados usuarios creados en todos lados, y porque todavía creemos que Instagram funciona de esa manera en que la gente se va a enterar de lo que hacés. Por ahora estamos en prueba beta para ver qué errores saltan.

Por ejemplo, hoy agregamos lo de la geolocalización automática, que para mí era central: si no, alguien entraba desde cualquier lugar del mundo y veía siempre el mapa situado en Buenos Aires. Ahora si lo abrís en Córdoba, ves varios puntitos y te despierta curiosidad. Pero tampoco puede llegar un aluvión masivo de golpe, porque no sabemos cuánta capacidad tiene el servidor sin tener que pagar más infraestructura. No está lista para que caigan 50.000 personas de golpe; cuando llegue el momento haremos una campaña más formal.

**[27:08] Constanza Chiappini (Coty):**
La adquisición de usuarios es lo más complejo. Primero porque la principal competencia es Instagram. Segundo, porque hay plataformas de portfolios de obra pagas, pero son muy caras en dólares y ninguna está en español ni piensa en nuestra realidad. Además funcionan con algoritmos. Mi idea con Vapor es recuperar la libertad de manejar los tiempos de exhibición de tu propia obra, sin demandas algorítmicas permanentes.

Convencer a la gente de que participe es complejo. En mi nicho, el arte contemporáneo, muchos artistas ya tienen galerías y descansan en que la galería muestra su obra. La idea es ampliar al público de artistas independientes y autónomos. Yo probé pagando publicidad en Instagram durante 15 días: funcionó para ganar seguidores y algunos usuarios, pero el cuello de botella es el modelo de negocio: Vapor tiene una versión gratis donde podés subir hasta 6 obras, y luego una membresía paga mediante suscripción mensual accesible para sostener el proyecto.

**[30:00] Sergio Scotta:**
Tiene un buscador por ciudad, ¿soporta que ponga 'cordoba' sin acento?

**[30:11] Constanza Chiappini (Coty):**
No.

**[30:11] Sergio Scotta:**
Eso después te ayudo, son dos liñitas de código.

**[30:11] Constanza Chiappini (Coty):**
O un prompt. Pasa que yo exageré con las cuestiones de seguridad: al no saber programar, pedí exceso de reglas.

**[30:43] Sergio Scotta:**
Y aun así es permeable, porque yo construí mi mapa haciendo scraping de tu sitio web: no puedo modificar nada, pero me nutro de tu información para generar conexiones.


## 7. El debate central: ¿Kiosquitos fragmentados o ecosistemas cooperativos?

**[31:03] Sergio Scotta:**
Esto me lleva a una pregunta central: ahora que es más fácil hacer aplicaciones con IA y que hay artistas haciendo software para artistas, se está empezando a crear un escenario muy fragmentado. Mucha gente haciendo herramientas donde cada uno tiene su propio 'quiosquito' desconectado.

Les dejo dos preguntas: primero, ¿el artista es la persona ideal para hacer aplicaciones para artistas? Y segundo: ¿creen que van a proliferar aplicaciones hechas con IA y se va a volver difícil comunicarnos, a diferencia de Instagram que con todos sus problemas nos reúne en un solo lugar?

**[33:01] Constanza Chiappini (Coty):**
Sobre Instagram: yo me fui durante seis meses y me dejé de enterar de absolutamente todo, así que no sé si es tan inclusivo como aparenta. Y sobre la fragmentación, el mundo del arte ya está fragmentado.

Respecto a programar con inteligencia artificial: la frustración aparece rápido porque creo que **la programación con IA tiene un techo bastante bajo**. Después se presentan problemas de seguridad, problemas de que querés cargar imágenes y revienta la capacidad del servidor... Al no ser nativo de la programación te das cuenta de que muchas cosas no funcionan. Y además es caro: mantener suscripciones de IA y servidores en la nube puede costarte 20 o 30 dólares mensuales durante meses. Por esa plata al final casi le pagás a un programador junior. Si no le dedicás muchísimo tiempo y trabajo neurótico, no lo vas a poder sostener.

**[36:33] Lola Granillo:**
Sobre si somos ideales o no, no lo sé. Yo prefiero hacer música, pero tampoco tengo ganas de estar trabajando para Instagram posteando cosas que después nadie mira en stories. Esto se volvió un proyecto que me divierte, y si no funciona de esta manera, funcionará de otra: hay plan B. Dentro del menú de la hamburguesa de Gotla también hay una idea de radio que todavía no existe pero puede ser.

Para mí se desarma la frontera entre si sos ideal o no, o si sos artista o programador: es parte de lo mismo. Hacer esta aplicación o hacer canciones es parte del mismo impulso creativo.

**[38:22] Constanza Chiappini (Coty):**
Muy poca gente piensa en los artistas más que los mismos artistas. Como estamos obligados al pluriempleo, terminás buscando soluciones a los problemas específicos que identificás en el sector. Al final somos los ideales porque no hay nadie más pensando en esto.

**[39:11] Sergio Scotta:**
La relación hoy es muy directa entre tener una necesidad y poder producir un sistema. A mí me encanta la idea de que hagamos cosas que nos ayuden a conectar en vez de aislarnos.

Por eso en mi proyecto pienso en un núcleo de conexiones: si Lola tiene un sistema con geolocalización, yo no me pongo a programar geolocalización, derivo a Gotla. Si Coty tiene portfolios, derivo a Vapor. Empezar a generar pequeños ecosistemas interconectados en Córdoba —como las fiestas de Electrosoma o el desfile de *Romper la Matriz*— unificando esfuerzos en vez de que cada uno esté solo en su individualidad.


## 8. Intervención del público: Economía de los dones y cooperativismo

**[42:50] Asistente del Público:**
Justo vengo de la asamblea y me resonaba mucho esto. Ustedes están usando la palabra 'ecosistema', y nosotros terminamos la charla hablando de la **economía de los dones** y de la lógica cooperativa. Es un poco lo que Sergio está trayendo: ¿para qué vas a invertir tiempo, dinero y energía en hacer algo que otra persona del colectivo ya resolvió?

No hay personas más idóneas que los artistas para entender los problemas de los artistas: conocemos la fibra fina de este lugar tan particular. Los modelos cooperativos me siguen pareciendo los más inteligentes. Si algo nos destaca a los artistas es que somos muy inteligentes. Re banco lo que dice Sergio: compartir herramientas, articular esfuerzos y aprender juntas en vez de duplicar trabajo.


## 9. Cierre y musicalización

**[45:35] Sergio Scotta:**
Bueno, antes de que el público muera de frío, vamos a darle espacio a quien quiera quedarse a escuchar la música en vivo de **Electrosoma**. Muchísimas gracias a todos por venir y nos vemos en la próxima edición.

**[52:14] Electrosoma:**
*(Inicio del set de música EBM / electrónica)*: *"This is a sound that creates a new dimension. This is a new style of music..."*
