odoo.define('falcon_material_backend_theme.logo_js', function (require) {
"use strict";
    var session = require('web.session');
    $(document).ready(function() {

          
        $('.hide_secondary').hide();
        $('.oe_secondary_menu_section').on('click',function() {
            if ($(this).attr('class') == 'oe_secondary_menu_section open_menu') {
                $('.oe_secondary_menu_section').removeClass('open_menu');
                $('.hide_secondary').hide();
            } else {
                $('.oe_secondary_menu_section').removeClass('open_menu');
                $('.hide_secondary').hide();
                next_element = $(this).next();
                if (next_element && next_element.attr('class') && next_element.attr('class') == 'oe_secondary_submenu nav nav-pills nav-stacked hide_secondary') {
                    next_element.show();
                    $(this).addClass('open_menu');
                }
            }
        });
        $('.o_sub_menu span.si-icons').on('click',
            function(e) {
                e.preventDefault(); // prevent the default action
                e.stopPropagation(); // stop the click from bubbling
                $('body').toggleClass('oe_leftbar_open');
            });
        
    });
     $(document).on('click', '.o_menu_header_lvl_2.mega_dropdown_menu span.third_level', function(e) { 
                    e.stopPropagation(); // stop the click from bubbling
                    e.preventDefault(); // prevent the default action

                    $(this).closest('a').next().toggleClass('show');
                    
    });
    $(document).on('click',function (e){
       if(e.target.id !== 'hideMe'){
           if($('#hideMe').hasClass('active'))
           {
                if ($("ul.o_menu_apps").has("div").length == 0){
                        $(".tag-less-more").wrapAll("<div class='more_item'></div>");    
                    }
                    $("ul.o_menu_apps li.tag-less-more").toggleClass('o_hidden');
                    $("ul.o_menu_apps a.more_disp").toggleClass('active'); 
           }
           
       }

    }); 


    $(document).on('click', 'a.more_disp', function(e) { 
        if ($("ul.o_menu_apps").has("p").length == 0){
            $(".tag-less-more").wrapAll("<p class='more_item'></p>");    
        }
        $("ul.o_menu_apps li.tag-less-more").toggleClass('o_hidden');
        $("ul.o_menu_apps a.more_disp").toggleClass('active');
    });
    waitForElementToDisplay(".o_theme_logo",100);
    function waitForElementToDisplay(selector, time) {
        if(document.querySelector(selector)!=null) {
            var state = $.bbq.getState();
            // If not set on the url, retrieve cids from the local storage
            // of from the default company on the user
            var current_company_id = session.user_companies.current_company[0]
            if (!state.cids) {
                state.cids = utils.get_cookie('cids') !== null ? utils.get_cookie('cids') : String(current_company_id);
            }
            var stateCompanyIDS = _.map(state.cids.split(','), function (cid) { return parseInt(cid) });
            var userCompanyIDS = _.map(session.user_companies.allowed_companies, function(company) {return company[0]});
            // Check that the user has access to all the companies
            if (!_.isEmpty(_.difference(stateCompanyIDS, userCompanyIDS))) {
                state.cids = String(current_company_id);
                stateCompanyIDS = [current_company_id]
            }
            // Update the user context with this configuration
            session.user_context.allowed_company_ids = stateCompanyIDS;
            $.bbq.pushState(state);
            $('.o_theme_logo').append('<a class="oe_logo_backend" href="/web"><img src="/web/image/res.company/' + stateCompanyIDS[0] + '/logo/"/></a>')
            if($(document).width() <768)
            {
              $(document).on('click', 'span.display_fa', function(e) { 
                    
                    $("ul.o_menu_systray").toggleClass('o_hidden');
                    $("#default_menu_data").toggleClass('o_hidden');            
                });
              $("#default_menu_data").toggleClass('o_hidden');  

            }
            else
            {
                $("ul.o_menu_systray").removeClass('o_hidden');

            }
            if($(document).width() <1100)
            {  
                $("#default_menu_data").css('display', 'block');
                $("ul.o_menu_apps li.demo").addClass('o_hidden');
                $("ul.o_menu_apps li.more_desk_toggle").addClass('o_hidden');


                $("ul.o_menu_apps li.tag-less-more").addClass('o_hidden');
            }
            else
            {
                 $("#default_menu_data").css('display', 'none');
                $("ul.o_menu_apps li.demo").removeClass('o_hidden');
                $("ul.o_menu_apps li.more_desk_toggle").removeClass('o_hidden');
            }
        }
        else {
            setTimeout(function() {
                waitForElementToDisplay(selector, time);
            }, time);
        }
    }
    function chkObject(elemClass)
    {
       return (document.getElementsByClassName(elemClass).length==1)? true : false;
    }
});
