package main

import (
	"fmt"
	"net/http"
	"strings"
)

func greet(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimPrefix(r.URL.Path, "/greet/")
	fmt.Fprintf(w, "Hello, %s!", name)
}

func main() {
	http.HandleFunc("/greet/", greet)
	http.ListenAndServe(":5555", nil)
}
