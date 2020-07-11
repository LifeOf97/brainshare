// make sure all resources are downloaded before running the javascript file 
$( document ).ready(function() {
    console.log("ALL IS WELL, THANK GOD.");

    const topNav = $("#topNav"), topNavLinks = $("#topNavLinks a");
    // variables for search form
    const searchBox = $("#searchBox"), openSearchBtn = $("#openSearchBtn"), closeSearchBtn = $("#closeSearchBtn");
    // variables for signed in user and side nav
    const user = $("#user"), userMenu = $("#userMenu"), closeUser = $("#closeUser");
    const mobileMenu = $("#mobileMenu"), mobileMenuBtn = $("#mobileMenuBtn"), clsMobileMenu = $("#clsMobileMenu");
    // hero variables
    const heroKnowledge = $("#heroKnowledge"), heroIs = $("#heroIs"), heroPower = $("#heroPower"), heroSignup = $("#heroSignup"),
    heroWorld = $("#heroWorld")
    // variables for  forms
    const inputLabel = $(".inputLabel"), viewPass = $(".viewPass");
    const formBox = $("#formBox"), signOutBox = $("#signOutBox"), signOutBtn = $("#signOutBtn");
    // variables for post detail
    const pageNumber = $("#pageNumber"), pageNumberBtn = $("#pageNumberBtn");
    // variables for posts list
    const postCard = $(".postCard"), copyBtn = $(".copyBtn"),
    postConcern = $("#postConcern a");
    // variables for dashboard
    const filterBtn = $("#filterBtn"), filterMenu = $("#filterMenu"), filter = $("#filterText"),
    filterOptions = $("#filterOptions"), mypost = $(".mypost"),
    dashboardBtn = $("#dashboardBtn"), dashboardTabs = $("#dashboardTabs");
    // variables for social form
    
    
    // hide elements that are hidden by default with css
    // with javascript also.
    userMenu.hide();
    signOutBox.hide();

    // third party plugins

    //global variable
    const localStorage = {
        'data': {}
    };

    
    // settings for topnav
    // show topnav when scroll up and hide when scroll down
    var preScrollPos = $(window).scrollTop();
    if (window.location.pathname.includes("dashboard") || window.location.pathname.includes("author")) {
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

    // this section deals with the home/landing/hero page/section
    const heroTimeline = gsap.timeline({defaults: {duration: 0.5, opacity: 0, ease: "power2"}});
    heroTimeline.from(heroKnowledge, {y: -50, delay: 1})
        .from(heroIs, {y: -50}, "+=0.2")
        .from(heroPower, {y: 100, ease: "back"}, "+=0.5")
        .from(heroSignup, {y: 100}, "+=1")
        .from(heroWorld, {y: 100}, "-=0.5")
    

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

    // function to copy the link of the post
    copyBtn.on("click", function() {
        var linkToCopy = $(this).parents("div.postCard").find(".title").attr("href");
        var keepCopy = $("<textarea>").attr("class", "copy opacity-0").text(window.location.host+linkToCopy);
        $(this).parents("div.postCard").append(keepCopy);
        keepCopy.select()
        document.execCommand("copy");
        $(this).parents("div.postCard").find("textarea.copy").remove();
    })
    
    // post details settings
    // show images with modal effects when clicked upon
    $(".image").on("click", function() {
        topNav.addClass("hidden");
        $("#postDetailContainer").addClass("opacity-25");
        $("#imageModal").attr("src", $(this).attr("src"));
        $("#modal").removeClass("hidden");
        gsap.from($("#imageModal"), {
            opacity: 0, scale: 0.2,
            duration: 0.5
        });
        gsap.from($("#closeModal"), {
            y: -60, duration: 0.5
        })
    });

    // function to close the image modal view
    $("#closeModal").on("click", function() {
        $("#modal").addClass("hidden");
        $("#postDetailContainer").removeClass("opacity-25");
        topNav.removeClass("hidden");
    });


    // pagination function to change the page to the number entered into
    // the field, i also converted the max attribute value of the input
    // field from string to number so as to make sure the value entered does
    // not exceed its max.    
    pageNumberBtn.on("click", function(event) {
        if ( (pageNumber.val() > 0) && (pageNumber.val() < pageNumber.attr("max")+1) ) {
            $(this).attr("href", "?page="+pageNumber.val());
        }
        else {
            event.preventDefault();
            $(this).attr("href", "?page="+pageNumber.attr("max"));
        }
    })

    pageNumber.on("keyup", function() {
        pageNumberBtn.attr("href", "?page="+$(this).val());
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
            filter.text("Draft");
            mypost.each(function() {
                if ($(this).find(".postStatus").text() == "Draft") {
                    $(this).removeClass("hidden");
                }
                else {
                    $(this).addClass("hidden");
                }
            });
            filterMenu.addClass("hidden")
            replaceClass(filterBtn, 'border-white', 'border-ph')
        }
        else if ($(this).text() == 'Published') {
            filter.text("Published");
            mypost.each(function() {
                if ($(this).find(".postStatus").text() == "Published") {
                    $(this).removeClass("hidden");
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


    // dashboard links settings to show its respective div content
    // when the specified link is clicked
    dashboardBtn.on("click", "input[type='button']", function() {
        // close the open tab
        dashboardTabs.children('div').each(function() {
            if ( !$(this).hasClass('hidden') ) {
                $(this).addClass('hidden')
            }
        });
        // remove the styling of active links
        dashboardBtn.children("input[type='button']").each(function() {
            replaceClass($(this), "text-white bg-body-500", "text-black bg-transparent")
        });
        // then open requested tab and style active link
        dashboardTabs.find('#'+$(this).attr('data-id')).removeClass('hidden')
        replaceClass($(this), 'text-black bg-transparent', 'text-white bg-body-500');
    });

    // dashboard forms settings functions
    $("#clsForm").on("click", function() {
        window.location.assign("/");
    })

    // message popup settings for form update and sign-in
    setTimeout(function() {
        if ($("#msg").length > 0) {
            gsap.to("#msgBox", {
                y: -50, opacity: 0, duration: 0.5,
                onComplete: function() { $("#msgBox").remove() }
            })
        }
    }, 4000)

    gsap.from("#msgBox", {
        y: -50, opacity: 0, duration: 0.5
    })

    // TOOLTIPS AND POPOVER MENU FUNCTIONS/SETTINGS
    //tippyjs to show tooltip on images
    tippy('.image', {
        content: "Click to view image in best possible size",
        followCursor: true,
        touch: false,
        theme: 'nav',
        hideOnClick: true,
        moveTransition: 'transform 0.2s ease-out',
    });

    // all html element with data-tippy-content
    tippy('[data-tippy-content]', {
        trigger: 'mouseenter click',
        theme: 'light',
    });
    
    // settings for all authors ajax tooltip 
    // set the global url variable to be used by the tippyjs to render a tooltip
    // for each post author
    $(".authorTooltipBtn").on("mouseenter", function() {
        // make the url variable a global one  so it can be accessed from other
        // function and all
        url = $(this).attr("href");
    })

    // the tooltip div that holds the result of the ajax call
    let authorTooltip = $(".authorTooltip");

    // tippyjs settings, at first display a loading screen then make the ajax call
    // with the tippyjs onShown prop and then display the returned data, when the tooltip
    // is closed revert back to the loading screen.
    tippy("#authorTooltipBtn", {
        content: 'Loading...',
        trigger: 'mouseenter',
        allowHTML: true,
        interactive: true,
        animation: 'scale',
        placement: 'top',
        theme: 'nav',
        delay: [200, 500],
        duration: [500, null],
        popperOptions: {
            modifiers: [
                {
                    name: 'flip',
                    options: {
                        fallbackPlacements: ['bottom', 'right'],
                    },
                },
                {
                    name: 'preventOverflow',
                    options: {
                        mainAxis: true,
                        altAxis: true,
                    }
                }
            ],
        },
        onShown(instance) {
            // tippyjs prop to change the tooltip when the ajax call is successfull
            let tooltipImage = $("#tooltipImage");
            let tooltipUsername = $("#tooltipUsername");
            let tooltipBio = $("#tooltipBio");
            let tooltipSocial = $("#tooltipSocial a");

            tooltipSocial.each(function() {
                // reset all social links and hide them
                $(this).attr("href", "").addClass("hidden");
            })

            function insertDetails(data) {
                // function to insert retrieved ajax data to appropriate location
                tooltipImage.attr('src', "/media/"+data.image);
                tooltipBio.text(truncateString(data.about_me, 129));
                tooltipUsername.text(truncateString(data.username, 10)).attr("href", data.author_url);
                // social data
                $.each(data.social.slice(0, 6), function(key, value) {
                    id = value['platform'].toLowerCase();
                    let social = document.getElementById(id)
                    social.setAttribute("href", value['link'])
                    social.classList.remove('hidden');
                })
            }

            if (!localStorage.data[url]) {
                ajaxRequest('GET', url, 'json', {'format': 'json'}, true);
            }
            else {
                insertDetails(localStorage.data[url])
                instance.setContent(authorTooltip.html());
            }
            
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
                    insertDetails(localStorage.data[url]);
                    instance.setContent(authorTooltip.html());
                })
                .fail(function(xhr, status, err) {
                    if (window.navigator.onLine) {
                        instance.setContent("An error occured");
                    }else {
                        instance.setContent("You are offline!");
                    }
                    console.log("An error occured");
                    // if the ajax reqeust fails, return an error message and add the url
                    // and undefined to the localStorage
                    localStorage.data[url] = undefined;
                    console.log("Status " + status);
                    console.log("Error " + err);
                    console.dir(xhr);
                });
            }

        },
        onHidden(instance) {
            // tippyjs prop to revert the tooltip back to the loading screen
            // when the tooltip is back to hidden
            instance.setContent("Loading...");
        }
    })
    //END OF TOOLTIP POPOVER MENU FUNCTIONS/SETTINGS

    
    // function to get users details and insert it into the dom,
    // first check if the data has been saved in the localStorage
    // if yes, use the saved data to fill the dom. else make a new ajax
    // request and save to the localstorage then fill the dom.

    $(".profileUser").on("click", function() {
        var url = $(this).attr("data-url");

        if (localStorage.data[url]) {
            insertData(localStorage.data[url]);
        }
        else {
            ajaxRequest2('GET', url, 'json', {'format': 'json'}, true);
        }
    });

    // // ajax request
    function ajaxRequest2(method, url, dataType, data, cache, img) {
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
    }

    // User defined reusable functions
    function replaceClass(obj, toRemove, toAdd) {
        // replace a class with another
        obj.removeClass(toRemove).addClass(toAdd);
    }

    // function to close the user menu dropdown
    function closerUserMenu(obj) {
        replaceClass(obj, "border-white", "border-transparent");
        userMenu.slideUp(100, function() {
            replaceClass(userMenu, "", "hidden");
        });
    }

    // function to truncate strings
    function truncateString(data, num) {
        if (data !== "") {
            if (data.length <= num) {
                return data;
            }
            else {
                return data.slice(0, num) + '...';
            }
        };
        return "";
    }
    
});
