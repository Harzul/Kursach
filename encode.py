import gfBasicMath as GFM
import gfPolyMath as GFPM


def rs_generator_poly(nsym, V):
    g = [1]
    for i in range(nsym):
        g = GFPM.gfPolyMul(g, [1, GFM.gfPow(V.generator, i, V)], V)
    return g


def rs_encode_msg(msg_in, nsym, V):
    if (len(msg_in) + nsym) > V.fieldChar: raise ValueError(
        "Message is too long (%i when max is %i)" % (len(msg_in) + nsym,  V.fieldChar))
    gen = rs_generator_poly(nsym, V)
    print(gen)
    msg_out = msg_in + [0] * (len(gen) - 1)
    lgen = [V.gfLog[gen[j]] for j in range(len(gen))]
    msg_in_len = len(msg_in)
    gen_len = len(gen)
    for i in range(msg_in_len):
        coef = msg_out[i]
        if coef != 0:
            lcoef = V.gfLog[coef]
            for j in range(1, gen_len):
                msg_out[i + j] ^= V.gfExp[lcoef + lgen[j]]
    msg_out[:msg_in_len] = msg_in
    return msg_out


def rs_calc_syndromes(msg, nsym, V, fcr=0):
    return [0] + [GFPM.gfPolyEval(msg, GFM.gfPow(V.generator, i + fcr, V), V) for i in range(nsym)]

