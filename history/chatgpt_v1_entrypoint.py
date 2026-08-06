"""Historical ChatGPT entry point for the canonical summation lesson.

The reusable implementation lives in :mod:`demos.summing_methods`.  This
small wrapper preserves the historical filename while ensuring that learners
run the maintained example rather than a separate copy of its logic.
"""

from demos.summing_methods import main

if __name__ == "__main__":
    main()
