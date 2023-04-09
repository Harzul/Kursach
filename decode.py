import gfBasicMath as GFM
import gfPolyMath as GFPM


class ReedSolomonError(Exception):
    pass


def rs_calc_syndromes(msg, nsym, V, fcr=0):
    return [0] + [GFPM.gfPolyEval(msg, GFM.gfPow(V.generator, i + fcr, V), V) for i in range(nsym)]


def rs_correct_errata(msg_in, synd, err_pos, V, fcr=0):
    msg = msg_in

    coef_pos = [len(msg) - 1 - p for p in err_pos]
    err_loc = rs_find_errata_locator(coef_pos, V)
    err_eval = rs_find_error_evaluator(synd[::-1], err_loc, len(err_loc) - 1,V)[::-1]

    X = [0]*len(coef_pos)
    for i in range(len(coef_pos)):
        l = V.fieldChar - coef_pos[i]
        X[i] = GFM.gfPow(V.generator, -l, V)

    E = [0]*len(msg)
    X_len = len(X)
    for i, Xi in enumerate(X):

        Xi_inv = GFM.gfInverse(Xi, V)

        err_loc_prime = 1
        for j in range(X_len):
            if j != i:
                err_loc_prime = GFM.gfMul(err_loc_prime, GFM.gfSub(1, GFM.gfMul(Xi_inv, X[j], V)), V)

        if err_loc_prime == 0:
            raise ReedSolomonError(
                "Decoding failed: Forney algorithm could not properly detect where the errors are located (errata locator prime is 0).")

        y = GFPM.gfPolyEval(err_eval[::-1], Xi_inv, V)
        y = GFM.gfMul(GFM.gfPow(Xi, 1 - fcr, V), y, V)

        magnitude = GFM.gfDiv(y, err_loc_prime, V)
        E[err_pos[i]] = magnitude
    msg = GFPM.gfPolyAdd(msg, E)
    return msg


def rs_find_error_locator(synd, nsym, V, erase_loc=None, erase_count=0):
    if erase_loc:
        err_loc = erase_loc
        old_loc = erase_loc
    else:
        err_loc = [1]
        old_loc = [1]

    synd_shift = 0
    if len(synd) > nsym: synd_shift = len(synd) - nsym

    for i in range(nsym - erase_count):
        if erase_loc:
            K = erase_count + i + synd_shift
        else:
            K = i + synd_shift
        delta = synd[K]
        for j in range(1, len(err_loc)):
            delta ^= GFM.gfMul(err_loc[-(j + 1)], synd[K - j], V)

        old_loc = old_loc + [0]

        if delta != 0:
            if len(old_loc) > len(err_loc):
                new_loc = GFPM.gfPolyScale(old_loc, delta, V)
                old_loc = GFPM.gfPolyScale(err_loc, GFM.gfInverse(delta, V), V)
                err_loc = new_loc

            err_loc = GFPM.gfPolyAdd(err_loc, GFPM.gfPolyScale(old_loc, delta, V))

    for i, x in enumerate(err_loc):
        if x != 0:
            err_loc = err_loc[i:]
            break
    errs = len(err_loc) - 1
    if (errs - erase_count) * 2 + erase_count > nsym:
        raise ReedSolomonError("Too many errors to correct")

    return err_loc


def rs_find_errata_locator(e_pos, V):
    e_loc = [1]
    for i in e_pos:
        e_loc = GFPM.gfPolyMul(e_loc, GFPM.gfPolyAdd([1], [GFM.gfPow(V.generator, i, V), 0]), V)
    return e_loc


def rs_find_error_evaluator(synd, err_loc, nsym, V):
    remainder = GFPM.gfPolyMul(synd, err_loc, V)
    remainder = remainder[len(remainder) - (nsym + 1):]

    return remainder


def rs_find_errors(err_loc, nmess, V):
    err_pos = []
    for i in range(nmess):
        if GFPM.gfPolyEval(err_loc, GFM.gfPow(V.generator, i, V), V) == 0:
            err_pos.append(nmess - 1 - i)
    errs = len(err_loc) - 1
    if len(err_pos) != errs:
        raise ReedSolomonError("Too many (or few) errors found by Chien Search for the errata locator polynomial!")
    return list(err_pos)


def rs_forney_syndromes(synd, pos, nmess, V):
    erase_pos_reversed = [nmess - 1 - p for p in pos]

    fsynd = list(synd[1:])
    for i in range(len(pos)):
        x = GFM.gfPow(V.generator, erase_pos_reversed[i], V)
        for j in range(len(fsynd) - 1):
            fsynd[j] = GFM.gfMul(fsynd[j], x, V) ^ fsynd[j + 1]
    return fsynd


def rs_correct_msg(msg_in, nsym, V, fcr=0, erase_pos=None, only_erasures=False):
    if len(msg_in) > V.fieldChar:
        raise ValueError("Message is too long (%i when max is %i)" % (len(msg_in), V.fieldChar))

    msg_out = list(msg_in)
    if erase_pos is None:
        erase_pos = []
    else:
        if isinstance(erase_pos, list):
            erase_pos = list(erase_pos)
        for e_pos in erase_pos:
            msg_out[e_pos] = 0

    if len(erase_pos) > nsym: raise ReedSolomonError("Too many erasures to correct")

    synd = rs_calc_syndromes(msg_out, nsym, V, fcr)

    if max(synd) == 0:
        return msg_out[:-nsym], msg_out[-nsym:], erase_pos  # no errors

    if only_erasures:
        err_pos = []
    else:

        fsynd = rs_forney_syndromes(synd, erase_pos, len(msg_out), V)

        err_loc = rs_find_error_locator(fsynd, nsym, V, erase_count=len(erase_pos))

        err_pos = rs_find_errors(err_loc[::-1], len(msg_out), V)
        if err_pos is None:
            raise ReedSolomonError("Could not locate error")

    msg_out = rs_correct_errata(msg_out, synd, erase_pos + err_pos, V, fcr)
    synd = rs_calc_syndromes(msg_out, nsym, V, fcr)
    if max(synd) > 0:
        raise ReedSolomonError("Could not correct message")

    return msg_out[:-nsym], msg_out[-nsym:], erase_pos + err_pos
