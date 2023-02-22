odoo.define('falcon_material_backend_theme.backend_falcon_theme', function(require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var Menu = require('web.Menu');
    var web_client = require('web.web_client');
    var ajax = require('web.ajax');
    $(document).ready(function() {
        if ($("div.o_main").length == 0){
            waitForElementToMainMenu(".o_action_manager",400);
            function waitForElementToMainMenu(selector, time) {
                if(document.querySelector(selector)!=null) {
                    $(".o_sub_menu,.o_action_manager").wrapAll("<div class='o_main'></div>");
                }
                else {
                    setTimeout(function() {
                        waitForElementToMainMenu(selector, time);
                    }, time);
                }
            }
        }
        $('.o_sub_menu').prepend("<span class='si-icons'><span></span><span class='s2'></span><span></span></spn>");

        $('.o_sub_menu span.si-icons').click(
            function(e) {
                e.preventDefault(); // prevent the default action
                e.stopPropagation(); // stop the click from bubbling
                $('body').toggleClass('oe_leftbar_open');
            });
        setTimeout(function(){
            ajax.jsonRpc('/get_apps/menu','call',{}).then( function(res){
            $('.o_main_navbar').find('ul.o_menu_sections').append(res);
            });
        }, 400);

    });
    return Menu.include({
        change_menu_section: function (primary_menu_id) {
            var res = this._super.apply(this, arguments);
            if (this.$menu_sections[primary_menu_id])
            {
                this.$menu_sections[primary_menu_id].appendTo($('div.o_sub_menu > .o_sub_menu_content > ul.oe_secondary_menu'));    
                if($("ul.oe_secondary_menu").has("li").length == 0) {
                     $(".o_sub_menu").addClass('o_hidden');
                }
                else
                {
                     $(".o_sub_menu").removeClass('o_hidden');
                }
            }
            
            return res
        },
        reflow: function(behavior) {
            var self = this;
            var $more_container = this.$('#menu_more_container').hide();
            var $more = this.$('#menu_more');
            var $systray = this.$el.parents().find('.oe_systray');

            $more.children('li').insertBefore($more_container);  // Pull all the items out of the more menu

            // 'all_outside' beahavior should display all the items, so hide the more menu and exit
            if (behavior === 'all_outside') {
                // Show list of menu items
                self.$el.show();
                this.$el.find('li').show();
                $more_container.hide();
                return;
            }

            // Hide all menu items
            var $toplevel_items = this.$el.find('li').not($more_container).not($systray.find('li')).hide();
            // Show list of menu items (which is empty for now since all menu items are hidden)
            self.$el.show();
            $toplevel_items.each(function() {
                var remaining_space = self.$el.parent().width() - $more_container.outerWidth();
                self.$el.parent().children(':visible').each(function() {
                    remaining_space -= $(this).outerWidth();
                });

                if ($(this).width() >= remaining_space) {
                    return false; // the current item will be appended in more_container
                }
                $(this).show(); // show the current item in menu bar
            });
            $more.append($toplevel_items.filter(':hidden').show());
            $more_container.toggle(!!$more.children().length);
            // Hide toplevel item if there is only one
            var $toplevel = self.$el.children("li:visible");
            if ($toplevel.length === 1) {
                $toplevel.hide();
            }
        },     
    });
});
