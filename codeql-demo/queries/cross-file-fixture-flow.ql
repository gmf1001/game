/**
 * @name Cross-file synthetic fixture flow
 * @description Tracks fixed synthetic data through helper modules into an in-memory sink.
 * @kind problem
 * @problem.severity warning
 * @id local/python-cross-file-fixture-flow
 */

import python
import semmle.python.dataflow.new.TaintTracking

module FixtureConfig implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) {
    exists(Call call, Name name |
      call.getFunc() = name and
      name.getId() = "fixture_source" and
      source = DataFlow::exprNode(call)
    )
  }

  predicate isSink(DataFlow::Node sink) {
    exists(Call call, Name name |
      call.getFunc() = name and
      name.getId() = "fixture_sink" and
      sink = DataFlow::exprNode(call.getArg(0))
    )
  }
}

module FixtureFlow = TaintTracking::Global<FixtureConfig>;

from DataFlow::Node source, DataFlow::Node sink
where FixtureFlow::flow(source, sink)
select sink, "Synthetic fixture data reaches this in-memory sink from $@.", source, "fixture_source"
