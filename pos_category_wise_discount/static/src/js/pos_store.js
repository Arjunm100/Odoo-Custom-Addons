import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        var orderlines = this.get_order().get_orderlines();
        var status = true;
        for(var i=0;i<orderlines.length;i++){
            var category = orderlines[i].models["pos.config"].getFirst()._raw.discount_categ_id;
            var discount_limit = (orderlines[i].models["pos.config"].getFirst()._raw.discount_categ_limit)*100;
            var product = orderlines[i].get_product();
            var line_discount = orderlines[0].get_discount();
            console.log(discount_limit)
            var discount_category = [];
            for(var j=0;j<product.pos_categ_ids.length;j++){
                discount_category.push(product.pos_categ_ids[j].id);
                }
            if(discount_category.includes(category)){
                if(line_discount > discount_limit){
                    status = false;
                    break;
                }
            }
        }
        if(status){
            return super.pay();
        }
        else{
            this.dialog.add(AlertDialog, {
                        title: _t("Warning"),
                        body: _t("The applied discount exceeds the allowed limit for this category."),
                    });
        }
    }
})

