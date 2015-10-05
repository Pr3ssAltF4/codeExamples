package perp;

/**
 * Share code for dealing with input errors
 *
 * @author James Heliotis
 */
public class Errors {

    /**
     * Report an error and stop the program. All output goes to standard error.
     *
     * @param msg The message to be printed first
     * @param info if not null, an additional value to be printed after a colon
     */
    public static void error( String msg, Object info ) {
        System.err.print( msg );
        if ( info != null ) {
            System.err.print( ": " + info );
        }
        System.exit( 2 );
    }
}
