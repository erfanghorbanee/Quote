// when click on tags
function post_by_tag(id) {

    const data = {
        requestType: 'getPostByTag'
    }

    $.ajax({
        type: "GET",
        enctype: 'multipart/form-data',
        url: "/tag-posts/" + id,
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
        success: function(data) {
            // clear current posts
            $('#content').html("");

            // add posts by tag
            for (let post in data) {
                var title = data[post].title
                var title2 = title.charAt(0).toUpperCase() + title.slice(1);

                var content = `<div class="col-md-12 ">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative ">
                    <div class="col p-4 d-flex flex-column position-static ">
                        <h3 class="mb-0 ">` + title2 + `</h3>
                        <div class="mb-1 text-muted ">` + data[post].pub_date + `</div>
                        <p class="card-text mb-auto ">` + data[post].content.substring(0, 300) + `</p>
                        <a href="/post/` + data[post]._id + `" class="stretched-link ">Continue
                                    reading</a>
                    </div>
                    <div class="col-auto d-none d-lg-block ">
                        <img src="static/images/posts_images/` + data[post].image + `" alt="post image" class="bd-placeholder-img">
            
                    </div>
                </div>
            </div>`

                $('#content').append(content);

            }
        },
        error: function(e) {
            console.log("ERROR : ", e);
        }
    });
};



// search
function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;

                    // get post by title from database
                    const data = {
                        requestType: 'getPostByTag'
                    }

                    $.ajax({
                        type: "GET",
                        enctype: 'multipart/form-data',
                        url: "/api/search/" + inp.value,
                        data: data,
                        processData: false,
                        contentType: false,
                        cache: false,
                        timeout: 600000,
                        success: function(data) {
                            // clear current posts
                            $('#content').html("");

                            // add posts by tag
                            for (let post in data) {
                                var title = data[post].title
                                var title2 = title.charAt(0).toUpperCase() + title.slice(1);
                                // console.log(data[post]._id);

                                var content = `<div class="col-md-12 ">
                                                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative ">
                                                    <div class="col p-4 d-flex flex-column position-static ">
                                                        <h3 class="mb-0 ">` + title2 + `</h3>
                                                        <div class="mb-1 text-muted ">` + data[post].pub_date + `</div>
                                                        <p class="card-text mb-auto ">` + data[post].content.substring(0, 300) + `</p>
                                                        <a href="/post/` + data[post]._id + `" class="stretched-link ">Continue
                                                                    reading</a>
                                                    </div>
                                                    <div class="col-auto d-none d-lg-block ">
                                                        <img src="static/images/posts_images/` + data[post].image + `" alt="post image" class="bd-placeholder-img">
                                    
                                                    </div>
                                                </div>
                                            </div>`

                                $('#content').append(content);

                            }
                        },
                        error: function(e) {
                            console.log("ERROR : ", e);
                        }
                    });

                    $('#search').val('');


                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}



/*initiate the autocomplete function on the "search" element, and pass along the title_list array as possible autocomplete values:*/
$("#search").on("input", function(event) {
    var title_list = [];

    let titles = document.getElementsByName('titles');
    titles.forEach((title) => {
        title_list.push(title.value);
    })

    autocomplete(document.getElementById("search"), title_list);
});