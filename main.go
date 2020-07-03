package main

import (
	"encoding/json"
	"fmt"
	"os/exec"
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
	program := "pip3"
	cmd := exec.Command(program, "install", "-r", "requirements.txt")
	fmt.Println("command args:", cmd.Args)
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Concatenation failed with error:", err.Error())
		return
	}
	print(out)

	keywords := []string{"corona", "covid"}

	for _, v := range keywords {
		search(v)
	}
}

func search(keyword string) {
	program := "python3"
	filename := "linkedin.py"
	cmd := exec.Command(program, filename, keyword)
	fmt.Println("command args:", cmd.Args)
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Concatenation failed with error:", err.Error())
		return
	}
	var a LinkedInResponse
	json.Unmarshal(out, &a)
	fmt.Println(a.Data)
}
