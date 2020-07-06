package main

import (
	"github.com/oazeus/scraper/pkg/fb/v1"
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
	keywords := []string{"corona", "nike"}
	posts, _ := v1.SearchFacebookPosts(keywords, 2)
	for _, post := range posts {
		// fmt.Println(string(post))
	}
}
