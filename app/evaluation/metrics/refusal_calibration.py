from typing import List, Dict, Any

def evaluate_refusal_and_temporal_calibration(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Computes precision & recall for refusal detection and post-2015 temporal detection across evaluation results.
    Returns 4 explicit numbers:
    - refusal_precision
    - refusal_recall
    - post_2015_precision
    - post_2015_recall
    """
    tp_refusal = 0
    fp_refusal = 0
    fn_refusal = 0

    tp_post_2015 = 0
    fp_post_2015 = 0
    fn_post_2015 = 0

    for item in results:
        expected_cat = item.get("expected_category")
        actual_refusal = item.get("is_refusal", False)
        actual_post_2015 = item.get("is_post_2015_inference", False)

        # Refusal metric tracking
        if actual_refusal:
            if expected_cat == "refusal":
                tp_refusal += 1
            else:
                fp_refusal += 1
        elif expected_cat == "refusal":
            fn_refusal += 1

        # Post-2015 metric tracking
        if actual_post_2015:
            if expected_cat == "post_2015":
                tp_post_2015 += 1
            else:
                fp_post_2015 += 1
        elif expected_cat == "post_2015":
            fn_post_2015 += 1

    refusal_precision = tp_refusal / float(tp_refusal + fp_refusal) if (tp_refusal + fp_refusal) > 0 else 1.0
    refusal_recall = tp_refusal / float(tp_refusal + fn_refusal) if (tp_refusal + fn_refusal) > 0 else 1.0

    post_2015_precision = tp_post_2015 / float(tp_post_2015 + fp_post_2015) if (tp_post_2015 + fp_post_2015) > 0 else 1.0
    post_2015_recall = tp_post_2015 / float(tp_post_2015 + fn_post_2015) if (tp_post_2015 + fn_post_2015) > 0 else 1.0

    return {
        "refusal_precision": round(refusal_precision, 4),
        "refusal_recall": round(refusal_recall, 4),
        "post_2015_precision": round(post_2015_precision, 4),
        "post_2015_recall": round(post_2015_recall, 4),
    }
