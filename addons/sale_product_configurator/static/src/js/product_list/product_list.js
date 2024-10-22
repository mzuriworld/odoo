/** @odoo-module */

import { Component } from "@odoo/owl";
import { formatCurrency } from "@web/core/currency";
import { Product } from "../product/product";

export class ProductList extends Component {
    static components = { Product };
    static template = "saleProductConfigurator.productList";
    static props = {
        products: Array,
        areProductsOptional: { type: Boolean, optional: true },
        step: { type: Number, default: 0, optional: true },
    };
    // static step = 0;
    static defaultProps = {
        areProductsOptional: false,
    };

    /**
     * Return the total of the product in the list, in the currency of the `sale.order`.
     *
     * @return {String} - The sum of all items in the list, in the currency of the `sale.order`.
     */
    getFormattedTotal() {
//        console.log(this.props.step);
        return formatCurrency(
            this.props.products.reduce(
                (totalPrice, product) => totalPrice + product.price * product.quantity, 0
            ),
            this.env.currencyId,
        )
    }
}
