import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    getDisplayData() {
        var data = super.getDisplayData();
        data['product_rating'] = this.get_product().pos_rating;
        return data;
    }
})
