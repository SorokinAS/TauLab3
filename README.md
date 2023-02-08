# Theory-of-automatic-control

My first experience using Go. Used Go 1.19.3. 

The system was designed in Matlab and a PID controller was implemented in Go. 

Input: data from Matlab
Output: the magnitude of the control action and the value to which the system should strive

Communication with Matlab is implemented using UDP sockets.


![изображение](https://user-images.githubusercontent.com/90500480/217546505-4aadb6b9-1a68-4c38-8fd8-67e1b61b85d4.png)
Scheme of the system.


![изображение](https://user-images.githubusercontent.com/90500480/217547543-a99508d4-fa6f-4ab5-94fc-1ddfddabe425.png)
Graph in Matlab with a setpoint of 500

![изображение](https://user-images.githubusercontent.com/90500480/217547809-53230c78-c301-436a-9ff1-9021b3afa329.png)
Graph in Matlab with a setpoint of 100

