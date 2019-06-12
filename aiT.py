import sys
import numpy as np
import skfuzzy as fuzz

def fuzzyBox(diff=0,discrim=0,guess=0):
    x_diff = np.arange(0, 11, 1)
    x_disc = np.arange(0, 11, 1)
    x_guess  = np.arange(0, 11, 1)
    x_score = np.arange(0, 11, 1)
    
    # Generate fuzzy membership functions
    diff_lo = fuzz.trimf(x_diff, [0, 0, 5])
    diff_md = fuzz.trimf(x_diff, [0, 5, 10])
    diff_hi = fuzz.trimf(x_diff, [5, 10, 10])
    disc_lo = fuzz.trimf(x_disc, [0, 0, 5])
    disc_md = fuzz.trimf(x_disc, [0, 5, 10])
    disc_hi = fuzz.trimf(x_disc, [5, 10, 10])
    guess_lo = fuzz.trimf(x_guess, [0, 0, 5])
    guess_md = fuzz.trimf(x_guess, [0, 5, 10])
    guess_hi = fuzz.trimf(x_guess, [5, 10, 10])
    score_lo = fuzz.trimf(x_score, [0, 0, 5])
    score_md = fuzz.trimf(x_score, [0, 5, 10])
    score_hi = fuzz.trimf(x_score, [5, 10, 10])

    diff_level_lo = fuzz.interp_membership(x_diff, diff_lo, diff)
    diff_level_md = fuzz.interp_membership(x_diff, diff_md, diff)
    diff_level_hi = fuzz.interp_membership(x_diff, diff_hi, diff)

    disc_level_lo = fuzz.interp_membership(x_disc, disc_lo, discrim)
    disc_level_md = fuzz.interp_membership(x_disc, disc_md, discrim)
    disc_level_hi = fuzz.interp_membership(x_disc, disc_hi, discrim)

    guess_level_lo = fuzz.interp_membership(x_guess, guess_lo, guess)
    guess_level_md = fuzz.interp_membership(x_guess, guess_md, guess)
    guess_level_hi = fuzz.interp_membership(x_guess, guess_hi, guess)

    part1 = min(diff_level_hi, min(disc_level_hi,guess_level_hi))
    part2 = min(diff_level_hi, min(disc_level_hi,guess_level_md))
    part3 = min(diff_level_hi, min(disc_level_hi,guess_level_lo))
    part4 = min(diff_level_md, min(disc_level_hi,guess_level_hi))
    part5 = min(diff_level_md, min(disc_level_hi,guess_level_md))
    part6 = min(diff_level_lo, min(disc_level_hi,guess_level_hi))

    active_rule1 = max(part1,part2,part3,part4,part5,part6)
    score_activation_hi = np.fmin(active_rule1, score_hi)

    part1 = min(diff_level_lo, min(disc_level_hi,guess_level_md))
    part2 = min(diff_level_md, min(disc_level_md,guess_level_hi))
    part3 = min(diff_level_hi, min(disc_level_md,guess_level_hi))
    part4 = min(diff_level_hi, min(disc_level_md,guess_level_md))
    part5 = min(diff_level_hi, min(disc_level_lo,guess_level_hi))
    part6 = min(diff_level_md, min(disc_level_hi,guess_level_lo))
    part7 = min(diff_level_md, min(disc_level_md,guess_level_md))
    part8 = min(diff_level_md, min(disc_level_md,guess_level_lo))
    part9 = min(diff_level_lo, min(disc_level_hi,guess_level_lo))

    active_rule2 = max(part1,part2,part3,part4,part5,part6,part7,part8,part9)
    score_activation_md = np.fmin(active_rule2, score_md)

    # low Difficult AND low interest AND far
    part1 = min(diff_level_lo, min(disc_level_lo,guess_level_lo))
    part2 = min(diff_level_hi, min(disc_level_md,guess_level_lo))
    part3 = min(diff_level_hi, min(disc_level_lo,guess_level_md))
    part4 = min(diff_level_hi, min(disc_level_lo,guess_level_lo)) 
    part5 = min(diff_level_md, min(disc_level_lo,guess_level_hi))
    part6 = min(diff_level_md, min(disc_level_lo,guess_level_md))
    part7 = min(diff_level_md, min(disc_level_lo,guess_level_lo))
    part8 = min(diff_level_lo, min(disc_level_md,guess_level_hi))
    part9 = min(diff_level_lo, min(disc_level_md,guess_level_md))
    part10 = min(diff_level_lo, min(disc_level_md,guess_level_lo))
    part11 = min(diff_level_lo, min(disc_level_lo,guess_level_hi))
    part12 = min(diff_level_lo, min(disc_level_lo,guess_level_md))

    active_rule3 = max(part1,part2,part3,part4,part5,part6,part7,part8,part9,part10,part11,part12)
    score_activation_lo = np.fmin(active_rule3, score_lo)
        
    score0 = np.zeros_like(x_score)

    # Aggregate all three output membership functions together
    aggregated = np.fmax(score_activation_lo,
                        np.fmax(score_activation_md, score_activation_hi))

    # Calculate defuzzified result
    score = fuzz.defuzz(x_score, aggregated, 'centroid')

    return (score)
  