package fb

import (
	"encoding/json"
	"fmt"
	"os/exec"
)

// post.post_id = post_id
// post.post_url = post_url
// post.profile_name = profile_name
// post.profile_link = profile_link
// post.caption = caption
// post.likes = likes
// post.comments = comments
// post.date_posted = date_posted
// post.post_images = post_images
// # post.content_html = content
// post.presentation = presentation
// post.type = "post"
// result.data.append(post)


// Post struct
type Post struct {
	ID string `json:"post_id"`,
}

func search(keyword string) {
	cmd := exec.Command("make", "fb_posts", "-e", "c="+keyword)
	fmt.Println("command args:", cmd.Args)
	out, err := cmd.CombinedOutput()

	print(out)
	if err != nil {
		fmt.Println("Concatenation failed with error:", err.Error())
		return
	}
	var a LinkedInResponse
	json.Unmarshal(out, &a)
	fmt.Println(a.Data)
}
