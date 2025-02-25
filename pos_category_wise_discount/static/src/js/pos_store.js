import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        var orderlines = this.get_order().get_orderlines();
        var category = [];
        this.config.pos_discount_wise_category_ids.forEach((categ) => {
            category.push(categ.id);
        })
        var discount_limit = (this.config.pos_discount_categ_limit)*100;
        var orderLineStatus = {'discount_price':0,'actual_price':0};
        orderlines.forEach((line) => {
            var product = line.get_product();
            var line_discount = line.get_discount();
            var discount_category = [];
            product.pos_categ_ids.forEach((categ) => {
                discount_category.push(categ.id);
            });
            if(discount_category.some(item => category.includes(item))){
                orderLineStatus['discount_price'] = orderLineStatus['discount_price'] + line.price_subtotal;
                orderLineStatus['actual_price'] = orderLineStatus['actual_price'] + ((line.price_subtotal)/((100-line_discount)/100));
            }
        });
        var discounted_total = ((orderLineStatus['actual_price'] - orderLineStatus['discount_price'])/orderLineStatus['actual_price'])*100;
        if(discounted_total <= discount_limit){
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
