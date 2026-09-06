// Local, deliberately narrow experiment. Included inside ConsumePartialTile.
#if TAIL_AB_ENABLED
    if constexpr (IsFirstTile && IsWarpReduction && ATTEMPT_VECTORIZATION
                  && NumThreads == 256 && ITEMS_PER_THREAD == 16 && vec_size == 4
                  && ::cuda::std::is_same_v<InputT, int> && ::cuda::std::is_same_v<AccumT, int>
                  && ::cuda::std::is_same_v<ReductionOp, ::cuda::std::plus<>>
                  && ::cuda::std::is_same_v<TransformOp, ::cuda::std::identity>)
    {
      // At least one complete vector per thread. Thus all 256 thread aggregates
      // remain valid for the unchanged collective-reduction call below.
      if (valid_items >= NumThreads * vec_size && IsAligned(d_in + block_offset))
      {
        CacheModifiedInputIterator<LOAD_MODIFIER, VectorT, OffsetT> vectors(
          reinterpret_cast<VectorT*>(const_cast<InputT*>(d_in) + block_offset));
        const int vector_count = valid_items / vec_size;
        int aggregate = 0; // Only the I32 plus/identity instantiation is supported.
        for (int v = static_cast<int>(lane_id); v < vector_count; v += NumThreads)
        {
          const VectorT value = vectors[v];
          aggregate += value.x;
          aggregate += value.y;
          aggregate += value.z;
          aggregate += value.w;
        }
        const int scalar_offset = vector_count * vec_size + static_cast<int>(lane_id);
        if (scalar_offset < valid_items)
        {
          aggregate += d_wrapped_in[block_offset + scalar_offset];
        }
        thread_aggregate = aggregate;
        return;
      }
    }
#endif
