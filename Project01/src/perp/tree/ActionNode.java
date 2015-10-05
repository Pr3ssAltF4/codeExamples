package perp.tree;

import perp.SymbolTable;

/**
 * A perp.tree.PerpNode that performs an action but does not
 * calculate a new value. The distinction between
 * ActionNode and ExpressionNode is only useful when
 * the nodes are directly executed by an interpreter.
 *
 * @author James Heliotis
 */
public interface ActionNode extends PerpNode {
    /**
     * Perform the action represented by this node. Actions are
     * things like changing variable values.
     * @param symTab the table where variable values are stored
     */
    void execute( SymbolTable symTab );
}
