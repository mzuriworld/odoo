/** @odoo-module */

import { registry } from "@web/core/registry";
import { many2OneField } from '@web/views/fields/many2one/many2one_field';
import { Component } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import  {  SaleOrderLineProductField } from '@sale/js/sale_product_field'


export class DuplicateProductDialog extends Component {
    static components = { Dialog };
    static props = {
        close: Function,
        title: String,
        orders: Array,
        onAddProduct: Function,
        onRemoveProduct: Function, 
   };
    static template = "mzuri_product_configurator.DuplicateProductDialog";
    setup() {
        this.title = this.props.title;            
    } 


    /**
     * @public
     */
    addProduct(orderId) {
        this.props.onAddProduct();
        this.props.close();
    }
    removeProduct() {   
        this.props.onRemoveProduct();       
    }
}

export class SaleOrderproductField extends SaleOrderLineProductField {
    setup() {
        super.setup();
        this.dialog = useService("dialog");       
    }

    async updateRecord (value){
        super.updateRecord(value);
        const is_duplicate = await this._onCheckproductUpdate(value);
    }

    async _onCheckproductUpdate(product) {     
        const partnerId = this.context.partner_id
        const customerName = document.getElementsByName("partner_id")[0].querySelector(".o-autocomplete--input").value;
        const productId = product[0];
        if (!customerName ) {
            alert("Please Choose Customer")
            return true; 
        }

        const saleOrderLines = await jsonrpc("/web/dataset/call_kw/sale.order.line/search_read", {
            model: 'sale.order.line',
            method: "search_read",
            args:  [
                [
                    ["order_partner_id", "=", partnerId],
                    ["product_template_id", "=", productId],
                    ["state","=","sale"]
                ]
            ],
            kwargs: {
                fields: ['id','product_uom_qty', 'order_id', 'move_ids', 'name', 'state'],
                order: "name"
            }
        });

        const reservedOrders = [];
        let stockMoves = [];
        if(saleOrderLines.length > 0){
            for (const line of saleOrderLines) {
                 const stockMoves = await jsonrpc("/web/dataset/call_kw/stock.move/search_read", {
                    model: 'stock.move',
                    method: "search_read",
                    args: [[
                        ['sale_line_id', '=', line.id],

                    ]],
                    kwargs: {
                        fields: ['name', 'state']
                    }
                });

                if (stockMoves.length > 0) {
                    reservedOrders.push({
                        order_number: line['order_id'][1],                       
                        order_id: line['order_id'][0],
                        product_info:line['name'],
                        product_qty: line['product_uom_qty']
                    });
                }               
            }        
        }

        if (reservedOrders.length > 0) {
            this.dialog.add(DuplicateProductDialog, {
                title: _t("Warning For %s", product[1]),
                orders: reservedOrders,      
                onAddProduct: async (product) => {
                    return true;
                },
                onRemoveProduct: async (product) => {
                    const currentRow = document.getElementsByClassName('o_data_row o_selected_row o_row_draggable o_is_false')[0]
                     if(currentRow){
                        currentRow.remove();                     
                     }    
                },
            });
            return true;
        } else {
            return false;
        }
    }
}
SaleOrderproductField.template = "web.Many2OneField";

export const saleOrderproductField = {
    ...many2OneField,
    component: SaleOrderproductField,
};

registry.category("fields").add("so_product_many2one", saleOrderproductField);