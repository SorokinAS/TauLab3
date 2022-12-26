package main

import (
	"encoding/binary"
	"log"
	"math"
	"net"
)

const (
	KP        = 0.04
	KI        = 0.00001
	KD        = 0.9
	SET_POINT = 500.0
)

func ByteToFloat(b []byte) float64 {
	bits := binary.LittleEndian.Uint64(b)
	return math.Float64frombits(bits)
}

func FloatToByte(f float64) []byte {
	var buf [8]byte
	binary.LittleEndian.PutUint64(buf[:], math.Float64bits(f))
	return buf[:]
}

func AddError(val float64, regError []float64) []float64 {
	regError = append(regError, val)
	if len(regError) > 2 {
		regError = regError[1:]
	}
	return regError
}

func SendSetPoint(addrSP *net.UDPAddr) {
	conn, err := net.DialUDP("udp", nil, addrSP)
	if err != nil {
		log.Fatal(err)
	}

	set := FloatToByte(SET_POINT)
	_, err = conn.Write(set)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {

	regError := make([]float64, 2)
	pidCtrl := 0.0
	reg := 0.0
	com := 0.0

	p := make([]byte, 8192)
	addrRecieve := net.UDPAddr{
		Port: 8080,
		IP:   net.ParseIP("127.0.0.1"),
	}
	addrSend := net.UDPAddr{
		Port: 8090,
		IP:   net.ParseIP("127.0.0.1"),
	}
	addrSendSetPoint := net.UDPAddr{
		Port: 9080,
		IP:   net.ParseIP("127.0.0.1"),
	}
	ser, err := net.ListenUDP("udp", &addrRecieve)
	if err != nil {
		log.Fatal(err)
	}
	conn, err := net.DialUDP("udp", nil, &addrSend)
	if err != nil {
		log.Fatal(err)
	}

	for {
		_, _, err := ser.ReadFromUDP(p)
		if err != nil {
			log.Fatal(err)
			continue
		}
		SendSetPoint(&addrSendSetPoint)
		com = ByteToFloat(p)
		regError = AddError(SET_POINT-com, regError)
		pidCtrl = KP*regError[1] + KI*(reg+regError[1]) + KD*(regError[1]-regError[0])
		reg = reg + regError[1]
		msg := FloatToByte(pidCtrl)
		_, err = conn.Write(msg)
		if err != nil {
			log.Fatal(err)
		}
	}
}
