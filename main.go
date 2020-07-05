package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"strings"
)

type LinkedInResponse struct {
	Code    string            `json:"code"`
	Message string            `json:"msg"`
	Data    []LinkedInCompany `json:"data"`
}

type LinkedInCompany struct {
	ID          string `json:id`
	Name        string `json:"name"`
	Link        string `json:"link"`
	Specialty   string `json:"specialty"`
	Followers   string `json:"followers"`
	Image       string `json:"image"`
	Description string `json:"description"`
}

func main() {
	keywords := []string{"corona", "covid"}
	toSearch := strings.Join(keywords[:], ",")
	go 
	quit := make(chan os.Signal)
	signal.Notify(quit, os.Interrupt)
	<-quit
}