
// make sure all resources are downloaded before running the javascript file 
$( document ).ready(function() {
    console.log("#@#@#@#@#@#All is well, Thank God@#@#@#@#@#@");

    const topNav = $("#topNav"), topNavLinks = $("#topNavLinks a");
    // variables for search form
    const searchBox = $("#searchBox"), openSearchBtn = $("#openSearchBtn"), closeSearchBtn = $("#closeSearchBtn");
    // variables for signed in user and side nav
    const user = $("#user"), userMenu = $("#userMenu"), closeUser = $("#closeUser"), accounts = $("#accounts");
    const mobileMenu = $("#mobileMenu"), mobileMenuBtn = $("#mobileMenuBtn"), clsMobileMenu = $("#clsMobileMenu");
    const profile = $("#profile"), openProfile = $("#openProfile"), closeProfile = $("#closeProfile");
    // variables for  forms
    const inputLabel = $(".inputLabel"), viewPass = $(".viewPass"), loadContainer = $("#loadContainer");
    const formBox = $("#formBox"), signOutBox = $("#signOutBox"), signOutBtn = $("#signOutBtn");
    // variables for post detail
    const pageNumber = $("#pageNumber"), pageNumberBtn = $("#pageNumberBtn");
    // variables for posts list
    const postCard = $(".postCard"), textContent = $(".textContent"), copyBtn = $(".copyBtn"),
    postConcern = $("#postConcern a");
    // variables for dashboard
    const filterBtn = $("#filterBtn"), filterMenu = $("#filterMenu"), filter = $("#filterText"),
    filterOptions = $("#filterOptions"), postStatus = $(".postStatus"), mypost = $(".mypost"),
    dashboardLinks = $("#dashboardLinks"), linkProfile = $("#linkProfile"), linkPost = $("#linkPost"),
    linkSetting = $("#linkSetting"), dashProfile = $("#dashProfile"), dashPosts = $("#dashPosts"),
    dashSettings = $("#dashSettings"), dashContainer = $("#dashContainer")
    // variables for social form
    
    
    // hide elements that are hidden by default with css
    // with javascript also.
    userMenu.hide();
    accounts.hide();
    profile.hide();
    signOutBox.hide();

    // third party plugins

    
    // settings for topnav
    // show topnav when scroll up and hide when scroll down
    var preScrollPos = $(window).scrollTop();
    if (window.location.pathname.includes("dashboard")) {
        null;
    }
    else {
        $(window).on("scroll", function() {
            var curScrollPos = $(window).scrollTop();
            if ( preScrollPos > curScrollPos) {
                topNav.removeClass("-top-20");
            }
            else {
                topNav.addClass("-top-20");
            }
            preScrollPos = curScrollPos;
        });
    }
    
    // changing the view of an active link
    topNavLinks.each(function() {
        if ($(this).attr("href") == window.location.pathname) {
            replaceClass($(this), "text-ph", "text-white bg-body-500");
        }
    })


    // open/close the search view for both desktop and mobile
    openSearchBtn.on("click", function() {
        if ( $(this).hasClass("text-button") ) {
            searchBox.slideDown(100);
            replaceClass($(this), "text-button", "text-white");
        }
        else {
            searchBox.slideUp(100);
            replaceClass($(this), "text-white", "text-button");
        }
    });

    closeSearchBtn.on("click", function() {
        searchBox.slideUp(100);
        replaceClass(openSearchBtn, "text-white", "text-button");
    });

    // toggle mobile menu view
    mobileMenuBtn.on("click", function() {
        if ( $(this).hasClass("border-transparent") ) {
            replaceClass($(this), "border-transparent", "border-white");
            mobileMenu.removeClass("hidden");
        }
        else {
            replaceClass($(this), "border-white", "border-transparent");
            mobileMenu.addClass("hidden");
        }
    });

    clsMobileMenu.on("click", function() {
        replaceClass(mobileMenuBtn, "border-white", "border-transparent");
        mobileMenu.addClass("hidden");
    });

    // open/close the user menu dropdown
    user.on("click", function() {
        if ($(this).hasClass("border-transparent")) {
            replaceClass($(this), "border-transparent", "border-white");
            userMenu.slideDown(100, function() {
                replaceClass(userMenu, "hidden");
            });
        }
        else {
            closerUserMenu($(this));
        }
    });

    closeUser.on("click", function() {
        closerUserMenu(user);
    });
    
    $(window).on("resize", function() {
        closerUserMenu(user);
    });

    // to open/close the profile view
    openProfile.on("click", function() {
        activateView(accounts);
        activateView(profile);
        closerUserMenu(user);
    });
    closeProfile.on("click", function() {
        deactivateView(profile);
        deactivateView(accounts);
    });


    /* these section of code runs only on form fields.
    it slides fieldlabel up when its input field is focused on
    and if field is empty when out of focus slide back down
    */
    // loop over all input labels and check if its input field has data
    // so as to keep the label field slide up
    inputLabel.each(function() {
        if ( $.trim($(this).next().val()).length > 0 ) {
            replaceClass($(this), "h-12", "h-8 -mt-6");
        }
    });
    // when an inputfield is clicked it is the labelfield on top
    // that recieves the event, so we slide it up and then give
    // focus to its input field
    inputLabel.on("click", function() {
        if ( $(this).hasClass("-mt-6 h-8") ) {
            null;
        }
        else {
            $(this).next(".txt").focus();
            replaceClass($(this), "h-12", "h-8 -mt-6");
        }
    });

    // this code block is used to slide up the inputlabel field
    // and give focus to its input field when keyboard keys like
    // the tab are used to navigate between fields 
    inputLabel.next(".txt").on("focusin", function() {
        replaceClass($(this).prev("div"), "h-12", "h-8 -mt-6");
    });
    // if an input field has no data when it goes out of focus
    // slide its label field back down
    inputLabel.next(".txt").on("focusout", function() {
        if ( $.trim($(this).val()).length < 1 ) {
            replaceClass($(this).prev("div"), "h-8 -mt-6", "h-12");
        }
    });

    // function to toggle view password
    viewPass.on("click", function() {
        if ( $(this).find("i").hasClass("fa-eye-slash") ) {
            replaceClass($(this).find("i"), "fa-eye-slash", "fa-eye");
            $(this).siblings("input").attr("type", "text");
        }
        else {
            replaceClass($(this).find("i"), "fa-eye", "fa-eye-slash");
            $(this).siblings("input").attr("type", "password");
        }
    });

    // buttons loading effect
    $("form").on("submit", function() {
        $(this).find("div#loadContainer").removeClass("hidden");
        gsap.to($(".loadicon"), 0.1, {
            scale: 1.5, yoyo: true, repeat: -1,
            stagger: 0.2
        })
    })


    // function to get the email address entered on the reset password
    // form and use that email in the resetpassword view
    var resetEmail = $("#resetEmail"), insertEmail = $("#insertEmail");
    var keepEmail = {
        "data": {}
    };
    resetEmail.parent().next().children("button").on("click", function() {
        const email = resetEmail.val();
        console.log(email);
        keepEmail.data["mail"] = email;
    });
    insertEmail.on("click", function() {
        console.dir(keepEmail);
    });

    // modal form effect
    // first effect is to open/close the sign out view with whatever effect
    // you like
    signOutBtn.on("click", function() {
        $("#container1").addClass("opacity-25");
        replaceClass(formBox, "hidden", "");
        signOutBox.slideDown(300);
    });
    $("#closeSignOut").on("click", function() {
        signOutBox.slideUp(300, function() {
            replaceClass(formBox, "", "hidden");
            $("#container1").removeClass("opacity-25");
        });
    });

    // post list settings
    // change the style of an active blog concern
    postConcern.each(function() {
        if ($(this).attr("href") == window.location.pathname) {
            replaceClass($(this), "text-button text-lg", "text-white text-2xl");
        }
    })

    // give slide effect to post text intro
    postCard.on("mouseenter", function() {
        gsap.from($(this).find(".textContent"), {
            y: 50, opacity: 0,
            duration: 0.5,
        })
    })
    
    // function to copy the link of the post to the clipboard
    copyBtn.on("click", function() {
        var linkToCopy = $(this).prev("div").find(".title").attr("href");
        var keepCopy = $("<textarea>").attr("class", "opacity-0").text("127.0.0.1:8000"+linkToCopy);
        $(this).parents().append(keepCopy);
        keepCopy.select()
        document.execCommand("copy");
        $(this).parents().children("textarea").remove()
    })

    // pagination function to change the page to the number entered into
    // the field, i also converted the max attribute value of the input
    // field from string to number so as to make sure the value entered does
    // not exceed its max.
    pageNumber.on("keyup", function() {
        pageNumberBtn.attr("href", "?page="+$(this).val());
    })
    
    pageNumberBtn.on("click", function(event) {
        if ( (+pageNumber.val() > 0) && (+pageNumber.val() < +pageNumber.attr("max")+1) ) {
            $(this).attr("href", "?page="+pageNumber.val());
        }
        else {
            event.preventDefault();
            console.log("Wrong Page number");
        }
    })

    // dashboard settings comes here
    // function to open/close the filter menu
    filterBtn.on("click", function() {
        if ($(this).hasClass("border-ph")) {
            filterMenu.removeClass("hidden")
            replaceClass($(this), 'border-ph', 'border-white')
        }
        else {
            filterMenu.addClass("hidden")
            replaceClass($(this), 'border-white', 'border-ph')
        }
    })

    // function to filter posts
    filterOptions.on("click", "button", function() {
        if ($(this).text() == 'Draft' ) {
            console.log("Turn to Draft");
            mypost.each(function() {
                if ($(this).find(".postStatus").text() == "Draft") {
                    $(this).removeClass("hidden");
                    filter.text("Draft");
                }
                else {
                    $(this).addClass("hidden");
                }
            });
            filterMenu.addClass("hidden")
            replaceClass(filterBtn, 'border-white', 'border-ph')
        }
        else if ($(this).text() == 'Published') {
            console.log("Turn to Published");
            mypost.each(function() {
                if ($(this).find(".postStatus").text() == "Published") {
                    $(this).removeClass("hidden");
                    filter.text("Published");
                }
                else {
                    $(this).addClass("hidden");
                }
            });
            filterMenu.addClass("hidden")
            replaceClass(filterBtn, 'border-white', 'border-ph')
        }
        else {
            mypost.removeClass("hidden");
            filter.text("All")
            filterMenu.addClass("hidden")
            replaceClass(filterBtn, 'border-white', 'border-ph')
        }
    })

    // dashboard forms settings functions
    $("#clsForm").on("click", function() {
        window.location.assign("/");
    })

    // dashboard links settings > move in panels with effect
    // when the specified link is clicked
    dashboardLinks.on("click", "a", function() {
        // remove the styling of active links first
        dashboardLinks.children().each(function() {
            replaceClass($(this), "text-white border-white", "text-black border-transparent")
        })
        // then run effect and style active link
        gsap.to(dashContainer, {
            scrollTo: $(this).attr("data-panel"),
            duration: 0.2,
            ease: "none",
            onStart: replaceClass($(this), "text-black border-transparent", "text-white border-white")
        })
    })

    
    // function to get users details and insert it into the dom,
    // first check if the data has been saved in the localStorage
    // if yes, use the saved data to fill the dom. else make a new ajax
    // request and save to the localstorage then fill the dom.
    const localStorage = {
        'data': {}
    };

    $(".profileUser").on("click", function() {
        var url = $(this).attr("data-url");

        if (localStorage.data[url]) {
            insertData(localStorage.data[url]);
        }
        else {
            ajaxRequest('GET', url, 'json', {'format': 'json'}, true);
        }
    });

    // ajax request
    function ajaxRequest(method, url, dataType, data, cache) {
        $.ajax({
            method: method,
            url: url,
            data: data,
            dataType: dataType,
            cache: cache,
        })
        .done(function(response) {
            console.log("Success response retrieved.");
            // if the ajax request was successful and returns an appropriate
            // response, add that url and its response to the localStorage
            localStorage.data[url] = response;
            insertData(localStorage.data[url]);
        })
        .fail(function(xhr, status, err) {
            console.log("An error occured");
            // if the ajax reqeust fails return an error message and add the url
            // and undefined to the localStorage
            localStorage.data[url] = undefined;
            console.log("Status " + status);
            console.log("Error " + err);
            console.dir(xhr);
        });
    }

    // function to insert users data to the dom
    function insertData(userData) {
        $("#numberOfPost").text(userData.number_of_post);
        $(".profileImg").attr("src", "/media/"+userData.image);
        $(".profileBanner").attr("src", "/media/"+userData.banner);
        $(".profileFullName").text(userData.first_name + " " + userData.last_name + " " + userData.other_name);
        $(".profileAlias").text(userData.username);
        $(".profileEmail").text(userData.email);
        $(".profileGender").text(userData.gender);
        $(".profileLocale").text(userData.state + ", " + userData.country);
        $(".profileJoined").text(userData.date_joined);
        $(".profileDob").text(userData.dob);
    }

    // User defined reusable functions
    function replaceClass(obj, toRemove, toAdd) {
        // replace a class with another
        obj.removeClass(toRemove).addClass(toAdd);
    }

    function activateView(obj) {
        // remove class 'hidden' from the element you will like to display
        replaceClass(obj, "hidden", "")
        // give any effect you wish on how the element should then be displayed
        obj.fadeIn(300)
    }

    function deactivateView(obj) {
        // give the effect you wish, on how the element should then be hidden
        obj.fadeOut(300, function() {
            // then add the hidden css class to the element
            replaceClass(obj, "", "hidden")
        })
    }

    // function to close the user menu dropdown
    function closerUserMenu(obj) {
        replaceClass(obj, "border-white", "border-transparent");
        userMenu.slideUp(100, function() {
            replaceClass(userMenu, "", "hidden");
        });
    }
});
