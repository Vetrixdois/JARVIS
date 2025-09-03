/*
  JARVIS Arduino Integration
  Controla LED que acende quando JARVIS está falando/ouvindo
  
  Conexões:
  - LED conectado no pino 13 (LED built-in do Arduino UNO)
  - Resistor de 220Ω se usar LED externo
  
  Comandos:
  - '1' = Liga LED
  - '0' = Desliga LED
*/

const int ledPin = 13;  // Pino do LED (built-in do Arduino UNO)

void setup() {
  // Inicializar comunicação serial
  Serial.begin(9600);
  
  // Configurar pino do LED como saída
  pinMode(ledPin, OUTPUT);
  
  // LED desligado no início
  digitalWrite(ledPin, LOW);
  
  // Sinal de inicialização (pisca 3 vezes)
  for(int i = 0; i < 3; i++) {
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
  
  Serial.println("Arduino JARVIS LED Controller Iniciado");
}

void loop() {
  // Verificar se há dados na serial
  if (Serial.available() > 0) {
    // Ler comando
    char comando = Serial.read();
    
    // Processar comando
    switch(comando) {
      case '1':
        // Ligar LED
        digitalWrite(ledPin, HIGH);
        Serial.println("LED ON");
        break;
        
      case '0':
        // Desligar LED
        digitalWrite(ledPin, LOW);
        Serial.println("LED OFF");
        break;
        
      default:
        // Comando desconhecido
        Serial.println("Comando desconhecido");
        break;
    }
  }
  
  // Pequeno delay para evitar spam
  delay(10);
}