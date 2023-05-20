/**
 * Pomoćna klasa koja enkapsulira parametre koje šalje korisnik. Instanca ove klase mora se proslijediti
 * kao lokalni parametar u .ejs datoteku pod ključem 'helper':
 * https://expressjs.com/en/4x/api.html#res
 *
 * ```
 * res.render('example', {
 *         ...
 *         helper: new Helper(parameters)
 *     });
 * });
 * ```
 *
 * Vaš zadatak je implementirati metode koje nisu implementirane unutar ove klase.
 * Nakon što se metode implementiraju, .ejs datoteka će se ispravno prikazati.
 * @type {Helper}
 */
module.exports = class Helper {

    constructor(params) {
        this.params = params;
    }


    /**
     * Metoda vraća niz koji je korisnik proslijedio za input
     * 'Where would you like to receive your newsletter? If left blank, we will use the one you have provided during registration.'
     * ili prazan string.
     * @returns {string|*}
     */
    email() {
        // ZADATAK
        if( this.params !== undefined && this.params.email !== undefined){

            return this.params.email;

        } else {
            return "";
        }
    }

    /**
     * Metoda vraća polje mogućih vrijednosti za input
     * 'Available newsletters:'
     * @returns {string[]}
     */
    newsletters() {
        // ZADATAK
        return ['None, thank you', 'All about seeds', 'Newest trends in gardening'];
    }



    /**
     * Za proslijeđeni parametar 'val', ova metoda vraća string 'selected' ako se 'val'
     * podudara s opcijom koju je korisnik odabrao za input
     * 'Available newsletters:'
     * , a inače vraća undefined.
     *
     * @param val input
     * @returns {string} 'selected' ili undefined
     */
    isNewsletterSelected(val) {
        // ZADATAK
        if(this.params !== undefined && this.params.newsletters == val){

            return 'selected';

        } else {
            return undefined;
        }
    }


    /**
     * Metoda vraća polje mogućih vrijednosti za input
     * 'Please confirm the following statements to continue:'
     * @returns {string[]}
     */
    statements() {
        // ZADATAK
        return ['I accept the terms and conditions', 'I have read the privacy policy'];
    }


    /**
     * Za proslijeđeni parametar 'val', ova metoda vraća string 'checked' ako se 'val'
     * podudara s opcijom koju je korisnik odabrao za input
     * 'Please confirm the following statements to continue:'
     * ,a inače vraća undefined.
     *
     * @param val input
     * @returns {string} 'checked' ili undefined
     */
    isStatementSelected(val) {
        // ZADATAK
        if(this.params !== undefined && this.params.statements !== undefined && this.params.statements.includes(val)){

            return 'checked';

        }   else {

            return undefined;
        }
    }

    /**
     * Metoda zamjenjuje znak razmaka ' ' u nizu sa '-' i pretvara string u mala slova
     * @param val input
     * @returns {string}
     */
    stringToHTMLId(val) {
        // NE TREBA implementirati
        return String(val).split(' ').join('-').toLowerCase();
    }

}
