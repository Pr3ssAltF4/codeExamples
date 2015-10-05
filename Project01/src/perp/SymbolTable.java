package perp;

import java.util.HashMap;
import java.util.Map;

/**
 * "Memory" for the Perp machine. A dictionary of variable names
 * and their current values.
 *
 * @author James Heliotis
 */
public class SymbolTable {

    private Map< String, Integer > table = new HashMap<>();

    /**
     * Create an empty symbol table. A new instance of
     * this class should be created every time execution
     * is about to start, be it interpretation of the tree
     * or execution of machine instructions.
     */
    public SymbolTable() {}

    /**
     * See if a variable is already in the table.
     * @param ident the identifier being checked
     * @return true iff ident is already in the table
     */
    public boolean exists( String ident ) {
        return table.containsKey( ident );
    }

    /**
     * Get the value of the given variable.
     * @rit.pre exists(ident)
     * @param ident the variable's name
     * @return the variable's value
     */
    public int get( String ident ) {
        if ( !table.containsKey( ident ) ) {
            Errors.error( "Non-existent variable", ident );
        }
        return table.get( ident );
    }

    /**
     * Assign the first, or a new, value to the given variable.
     * @param ident the variable's name
     * @param value the variable's new value
     */
    public void put( String ident, int value ) {
        table.put( ident, value );
    }

    /**
     * Show on standard output the values of all the variables in the table.
     */
    public void dump() {
        System.out.println( "Symbol Table Contents\n=====================\n" );
        for ( String ident: table.keySet() ) {
            System.out.printf( "%12s : %11d\n", ident, table.get( ident ) );
        }
    }
}
