package v1

import (
	"encoding/json"
	"fmt"
	"os/exec"
	"strconv"
)

//PostResponse struc
type PostResponse struct {
	Code    string `json:"code"`
	Message string `json:"msg"`
	Data    []Post `json:"data"`
}

// Post struct
type Post struct {
	ID       string `json:"post_id"`
	PostURL  string `json:"post_url"`
	Link     string `json:"link"`
	Video    string `json:"video"`
	Image    string `json:"image"`
	Text     string `json:"text"`
	Likes    int64  `json:"likes"`
	Comments int64  `json:"comments"`
	Shares   int64  `json:"shares"`
}

// SearchFacebookPosts return array of posts
func SearchFacebookPosts(keywords []string, pages int) ([]Post, error) {
	var res []Post
	if len(keywords) > 0 {
		for _, keyword := range keywords {
			posts, _ := execScript(keyword, pages)
			for _, post := range posts {
				res = append(res, post)
			}
		}
		return res, nil
	}

	return res, nil
}

func execScript(keyword string, pages int) ([]Post, error) {
	var res PostResponse
	cmd := exec.Command("python3", "./scripts/fb.py", "--keywords="+keyword, "--pages="+strconv.Itoa(pages))
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Concatenation failed with error:", err.Error())
		return res.Data, err
	}
	json.Unmarshal(out, &res)
	return res.Data, nil
}
