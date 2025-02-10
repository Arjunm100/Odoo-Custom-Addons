/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
import { redirect } from "@web/core/utils/urls"
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
function _generateId(){
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let id = '';
        for (let i = 0; i < 10; i++) {
            const randomIndex = Math.floor(Math.random() * characters.length);
            id += characters[randomIndex];
            }
        var new_id = Date.now().toString(36) + id;
        return new_id
}
var LatestAvailableProperty = PublicWidget.Widget.extend({
    selector : '.latest_property_snippet',
    events : {"click .property_card" : "redirectProperty"},
    willStart: async function () {
            const data = await rpc('/latest-property')
            this.property = {data}
            },
    start: function () {
    const refEl = this.$el.find("#latest_property_carousel")
    const property = this.property
    if(property['data'].length != 0){
        var property_data = _chunk(property['data'],4)
        var data = {property_data}
        var rendered_snippet = renderToElement('property.property_time_wise',data)
        refEl.html(rendered_snippet)
        var new_id2 = _generateId()
        var carousel_id = refEl.find('#prop_carousel')
        carousel_id.find('.carousel-control-prev').attr('href',`#${new_id2}`)
        carousel_id.find('.carousel-control-next').attr('href',`#${new_id2}`)
        carousel_id.attr('id',new_id2)
        var slides = refEl.find('.carousel-item')
        var new_id = _generateId()
        slides[0].id = new_id
        var slide = this.$el.find(`#${new_id}`)
        slide.addClass('active')
        var propertyCarousel = this.$el.find(".prop_carousel")
    }
    },
    redirectProperty : function (ev) {
    var property_id = ev.currentTarget.id
    console.log(property_id)
    redirect(`/property-data/${property_id}`)
    }
})
PublicWidget.registry.LatestPropertySnippet = LatestAvailableProperty;
return LatestAvailableProperty;