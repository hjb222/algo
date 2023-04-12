from typing import Literal
import beaker
import pyteal as pt




app = beaker.Application("ContractToContractExample")

@app.external
def add(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    """Add b to a"""
    return output.set(a.get() + b.get())

@app.external
def sub(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    """Subtract b from a"""
    return output.set(a.get() - b.get())

@app.external
def div(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    """Divide a by b"""
    return output.set(a.get() / b.get())

@app.external
def mul(a: pt.abi.Uint64, b: pt.abi.Uint64, *, output: pt.abi.Uint64) -> pt.Expr:
    """Multiply a and b"""
    return output.set(a.get() * b.get())


@app.external
def echo(v: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    """echos the string back unchanged"""
    return output.set(v)


@app.external
def call_calc_method(
    fn_selector: pt.abi.StaticBytes[Literal[4]], # method selector 
    a: pt.abi.Uint64,
    b: pt.abi.Uint64,
    other_app: pt.abi.Application,
    *,
    output: pt.abi.Uint64,
) -> pt.Expr:
    return pt.Seq(
        # call other app method, specified by fn
        # pass args a and b

        pt.InnerTxnBuilder.Begin(),
        pt.InnerTxnBuilder.SetFields({
            pt.TxnField.type_enum: pt.TxnType.ApplicationCall,
            pt.TxnField.application_id: other_app.application_id(),
            pt.TxnField.application_args: [
                fn_selector.encode(),
                a.encode(),
                b.encode(),
            ],
            pt.TxnField.fee: pt.Int(0),
        }),
        pt.InnerTxnBuilder.Submit(),
        output.decode(pt.Suffix(pt.InnerTxn.last_log(), pt.Int(4)))
    )


@app.external
def call_other_application(
    other_application: pt.abi.Application,
    string_to_echo: pt.abi.String,
    *,
    output: pt.abi.String,
) -> pt.Expr:
    """calls another contract and returns the result"""
    return pt.Seq(
        # Call the echo method on the other application
        pt.InnerTxnBuilder.ExecuteMethodCall(
            app_id=other_application.application_id(),
            method_signature=echo.method_signature(),
            args=[string_to_echo],
            extra_fields={
                # Set the fee to 0 so we don't have to
                # fund the app account. We'll have to cover
                # the fee ourselves when we call this method
                # from off chain
                pt.TxnField.fee: pt.Int(0),
            },
        ),
        # Set the output to whatever it sent us back
        output.set(pt.Suffix(pt.InnerTxn.last_log(), pt.Int(4))),
    )
