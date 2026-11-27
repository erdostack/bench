<?php

namespace App\Repositories;

use Illuminate\Support\Facades\DB;

class PartRepository
{
    public function find(int $partId): ?object
    {
        return DB::table('parts')->where('id', $partId)->first();
    }

    /** Parts that can be ordered today in place of $partId. */
    public function currentReplacements(int $partId): array
    {
        return DB::select('CALL resolve_current_parts(?)', [$partId]);
    }
}
