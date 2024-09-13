// Fuzzy logic variables
float e[5];
float edot[5];
float ce[5] = {-0.75, -0.25, 0, 0.25, 0.75}; // Error range for fuzzy logic
float cedot[5] = {-0.75, -0.42, 0, 0.42, 0.75}; // Error rate of change range for fuzzy logic

float y_out[7] = {-1, -0.8, -0.4, 0, 0.4, 0.8, 1}; // Output values for fuzzy logic

float y_temp[5][5]; // Temporary output values for fuzzy logic
float y_final; // Final output value

float beta[5][5];
float error = 0.5; // Example error value
float errordot = 0.1; // Example error rate of change value

// Function declarations
float triangularMembershipFunction(float x, float L, float C1, float C2, float R);
void fuzzyLogic();

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Update example error and error rate of change
  error = 1; // Increment error for demonstration
  //if (error > 1) error = -1; // Reset error for demonstration

  errordot = 0.01; // Increment error rate of change for demonstration
  //if (errordot > 1) errordot = -1; // Reset error rate of change for demonstration

  // Perform fuzzy logic calculation
  fuzzyLogic();

  // Print result
  Serial.print("Fuzzy Logic Output: ");
  Serial.println(y_final);

  // Delay for readability
  delay(1000); // Delay 1 second before next loop iteration
}

// Triangular membership function for fuzzy logic
float triangularMembershipFunction(float x, float L, float C1, float C2, float R) {
  float val;
  if (x < L) {
    val = 0;
  } else if (x < C1) {
    val = (x - L) / (C1 - L);
  } else if (x < C2) {
    val = 1;
  } else if (x < R) {
    val = (R - x) / (R - C2);
  } else {
    val = 0;
  }
  return val;
}

// Fuzzy logic calculation
void fuzzyLogic() {
  // Calculate membership values for error
  e[0] = triangularMembershipFunction(error, -3, -2, ce[0], ce[1]);   // NB
  e[1] = triangularMembershipFunction(error, ce[0], ce[1], ce[1], ce[2]);  // NS
  e[2] = triangularMembershipFunction(error, ce[1], ce[2], ce[2], ce[3]);      // ZE
  e[3] = triangularMembershipFunction(error, ce[2], ce[3], ce[3], ce[4]);     // PS
  e[4] = triangularMembershipFunction(error, ce[3], ce[4], 2, 3);      // PB

  // Calculate membership values for error rate of change
  edot[0] = triangularMembershipFunction(errordot, -3, -2, cedot[0], cedot[1]);   // NB
  edot[1] = triangularMembershipFunction(errordot, cedot[0], cedot[1], cedot[1], cedot[2]);  // NS
  edot[2] = triangularMembershipFunction(errordot, cedot[1], cedot[2], cedot[2], cedot[3]);      // ZE
  edot[3] = triangularMembershipFunction(errordot, cedot[2], cedot[3], cedot[3], cedot[4]);     // PS
  edot[4] = triangularMembershipFunction(errordot, cedot[3], cedot[4], 2, 3);      // PB

  // Compute beta values and fuzzy output
  float numerator = 0.0;
  float denominator = 0.0;

  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
      // Max-Product method for fuzzy logic
      beta[i][j] = e[i] * edot[j];

      // Define fuzzy rule outputs
      if (((i == 0) && (j == 0)) || ((i == 0) && (j == 1)) || ((i == 1) && (j == 0))) {
        y_temp[i][j] = y_out[0]; // NB
      } else if (((i == 2) && (j == 0)) || ((i == 1) && (j == 1)) || ((i == 0) && (j == 2))) {
        y_temp[i][j] = y_out[1]; // NM
      } else if (((i == 3) && (j == 0)) || ((i == 2) && (j == 1)) || ((i == 1) && (j == 2)) || ((i == 0) && (j == 3))) {
        y_temp[i][j] = y_out[2]; // NS
      } else if (((i == 4) && (j == 0)) || ((i == 3) && (j == 1)) || ((i == 2) && (j == 2)) || ((i == 1) && (j == 3)) || ((i == 0) && (j == 4))) {
        y_temp[i][j] = y_out[3]; // ZE
      } else if (((i == 4) && (j == 1)) || ((i == 3) && (j == 2)) || ((i == 2) && (j == 3)) || ((i == 1) && (j == 4))) {
        y_temp[i][j] = y_out[4]; // PS
      } else if (((i == 4) && (j == 2)) || ((i == 3) && (j == 3)) || ((i == 2) && (j == 4))) {
        y_temp[i][j] = y_out[5]; // PM
      } else {
        y_temp[i][j] = y_out[6]; // PB
      }

      // Calculate weighted average
      numerator += beta[i][j] * y_temp[i][j];
      denominator += beta[i][j];
    }
  }
  y_final = numerator / denominator;
}
