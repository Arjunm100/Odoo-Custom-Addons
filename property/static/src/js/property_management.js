/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { redirect } from "@web/core/utils/urls"
import { parseHTML } from "@html_editor/utils/html";
publicWidget.registry.web_form_template = publicWidget.Widget.extend({
    selector: "#property_order_tab",
    events: {
        'click .add_order_line' : "addOrderLine",
        "change select[name='property_orderline']" : "calculateAmount",
        "change select[name='order_type']" : "calculateAmount",
        "change input[name='start_date']" : "calculateAmount",
        "change input[name='end_date']" : "calculateAmount",
        "click .remove_line" : "onclickRemoveline",
        "click .create_order" : "onclickSubmit",
        "click .close-btn" : "closeAlertBox",
    },
    addOrderLine: function (ev) {
        var start_date = this.$el.find("input[name='start_date']").val();
        var end_date = this.$el.find("input[name='end_date']").val();
        if(start_date && end_date){
            var row_ids = []
            var rows = this.$el.find(".orderline_table").find("tr.added_order_lines")
            var emptyRow = false;
            for(var i=0; i < rows.length;i++){
                var value = this.$el.find(`tr#${rows[i].id}`);
                row_ids.push(rows[i].id)
                var property = value.find("select[name='property_orderline']").val();
                if(property === "['False', '', '', '']"){
                    emptyRow = true;
                    break;
                }
            }
            if(emptyRow){
                var alert_box = this.$el.find("div[name='property_alert_box']").show();
                alert_box.find("div[name='property_header']").text("Order line cannot be empty");
                alert_box.find("ul[name='property_ul']").text("Please add property in order lines");
                }
            else{
                var new_row = this.$el.find('tr.demo_order_lines').clone(true);
                const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                let id = '';
                for (let i = 0; i < 10; i++) {
                    const randomIndex = Math.floor(Math.random() * characters.length);
                    id += characters[randomIndex];
                    }
                var new_id = Date.now().toString(36) + id;
                new_row.removeClass('d-none');
                new_row.removeClass('demo_order_lines');
                new_row.addClass('added_order_lines');
                new_row.attr("id",new_id)
                new_row.insertBefore($('.demo_order_lines'));
            }
        }else{
            var alert_box = this.$el.find("div[name='property_alert_box']").show();
                alert_box.find("div[name='property_header']").text("Missing Dates :");
                alert_box.find("ul[name='property_ul']").text("Provide start date and end date to continue");
        }
    }
    ,
    calculateAmount: function (ev) {
        var start_date = this.$el.find("input[name='start_date']").val();
        var end_date = this.$el.find("input[name='end_date']").val();
        if(start_date && end_date){
            start_date = new Date(start_date);
            end_date = new Date(end_date);
            var days = (end_date.getTime() - start_date.getTime())/(1000 * 3600 * 24);
        }else{
            var days = 1;
        }
        this.$el.find("div[name='days_count']").empty().append(days);
        if(days>0){
            this.$el.find('tr.added_order_lines').show();
            if(this.$el.find('select#order_type').val() == 'rent'){
                var rent_lease = 2;}else{
                var rent_lease = 3;}
            var rows = this.$el.find(".orderline_table").find("tr.added_order_lines");
            if(rows.length){
                for(var i=0;i<rows.length;i++){
                    var value = this.$el.find(`tr#${rows[i].id}`);
                    var property = value.find("select[name='property_orderline']").val();
                    if(property != "['False', '', '', '']"){
                        property = property.replace(/'/g,'"');
                        property = JSON.parse(property);
                        var amount = property[rent_lease];
                        var total_amount = property[rent_lease]*days;
                        value.find("div[name='amount']").empty().append(amount);
                        value.find("div[name='total_amount']").empty().append(total_amount);
                    }
                    }
            }
        }else{
            this.$el.find('tr.added_order_lines').hide();
            var alert_box = this.$el.find("div[name='property_alert_box']").show();
            alert_box.find("div[name='property_header']").text("Invalid Input");
            alert_box.find("ul[name='property_ul']").text("End date cannot be past of start date");
            this.$el.find("input[name='end_date']").val('');
            this.$el.find("div[name='days_count']").text('');
        }
    },
    onclickRemoveline : function (ev) {
            ev.target.closest('tr').remove()
    },
    onclickSubmit: async function(ev) {
    var start_date = this.$el.find("input[name='start_date']").val();
    var end_date = this.$el.find("input[name='end_date']").val();
    if(start_date && end_date){
        var order_type = this.$el.find("select[name='order_type']").val();
        var rows = this.$el.find(".orderline_table").find("tr.added_order_lines");
        var properties = [];
        for (var i = 0; i < rows.length; i++) {
            var value = this.$el.find(`tr#${rows[i].id}`);
            var property = value.find("select[name='property_orderline']").val();
            property = property.replace(/'/g, '"');
            property = JSON.parse(property);
             if(property[0] !== "False"){
                properties.push(property[0]);
            }
            }
        var data = {'start_date':start_date,'end_date':end_date,'order_type':order_type,'properties':properties};
        rpc('/property/submit',{actions : data}).then(result => {redirect(`/thank-you/${result}`)})
    }else{var alert_box = this.$el.find("div[name='property_alert_box']").show();
              alert_box.find("div[name='property_header']").text("Missing Data");
              alert_box.find("ul[name='property_ul']").text("Please fill all the fields");}
    },
    closeAlertBox : function (ev) {
        var buttonId = ev.target.id
        var alert_box = this.$el.find('#'+buttonId).parent()
        alert_box.find("div[name='property_header']").text("");
        alert_box.find("ul[name='property_ul']").text("");
        alert_box.hide();
    },
});
