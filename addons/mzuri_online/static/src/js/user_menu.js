/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { UserMenu } from "@web/webclient/user_menu/user_menu";

patch(UserMenu.prototype, "mzuri_online.UserMenu", {
    setup() {
        this._super(...arguments);
        // Filter out "My Odoo.com account" menu item
        this.items = this.items.filter((item) => item.id !== "account");
    },
});
