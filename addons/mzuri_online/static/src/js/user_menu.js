/** @odoo-module **/

import { registry } from '@web/core/registry/user_menu';

function removeOdooAccountItem(env) {
    return {
        type: "item",
        id: "account",
        description: "My Odoo.com account",
        callback: () => {
            env.services.rpc("/web/session/account")
                .then((url) => {
                    window.open(url, "_blank");
                })
                .catch(() => {
                    window.open("https://accounts.odoo.com/account", "_blank");
                });
        },
        sequence: 60,
    };
}

// Remove the existing item by filtering it out
registry.category("user_menuitems").remove('account');
